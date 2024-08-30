import logging
import numpy as np
import pandas as pd
from typing import Any, Dict, Union, List, Optional, cast
from datetime import datetime, timezone
from dataclasses import dataclass
from datapipe.run_config import RunConfig
from datapipe.store.database import TableStoreDB

from sqlalchemy import Integer, Column, JSON, DateTime

from datapipe.types import (
    IndexDF,
    Labels,
    data_to_index,
    index_difference,
    index_to_data,
)
from datapipe.compute import (
    PipelineStep,
    DataStore,
    Table,
    Catalog,
    ComputeStep,
)
from datapipe.step.batch_transform import BatchTransformStep
from datapipe.step.datatable_transform import DatatableTransformStep
from datapipe.datatable import DataTable
from datapipe.store.database import DBConn
import label_studio_sdk._legacy as label_studio_sdk
from datapipe_label_studio_lite.sdk_utils import get_project_by_title, get_tasks_iter
from label_studio_sdk.data_manager import Filters, Operator, Type, DATETIME_FORMAT


logger = logging.getLogger("dataipipe_label_studio_lite")


@dataclass
class LabelStudioStep(PipelineStep):
    input: str  # Input Table name
    output: str  # Output Table name
    sync_table: str

    ls_url: str
    api_key: str
    dbconn: Union[DBConn, str]
    project_identifier: Union[str, int]  # project_title or id
    data_sql_schema: List[Column]

    name: Optional[str] = None

    project_label_config_at_create: str = ""
    project_description_at_create: str = ""

    create_table: bool = False
    delete_unannotated_tasks_only_on_update: bool = False

    labels: Optional[Labels] = None

    def __post_init__(self):
        assert self.dbconn is not None
        self.data_sql_schema: List[Column] = [column for column in self.data_sql_schema]
        self.data_sql_schema_primary: List[Column] = [
            column for column in self.data_sql_schema if column.primary_key
        ]
        self.data_columns: List[str] = [
            column.name for column in self.data_sql_schema if not column.primary_key
        ]
        self.primary_keys = [
            column.name for column in self.data_sql_schema if column.primary_key
        ]
        for column in ["task_id", "annotations"]:
            assert (
                column not in self.data_columns and column not in self.primary_keys
            ), f'The column "{column}" is reserved for this PipelineStep.'
        if isinstance(self.project_identifier, str):
            assert len(self.project_identifier) <= 50

        self.name_prefix = f"{self.name}_" if self.name is not None else ""

        # lazy initialization
        self._ls_client: Optional[label_studio_sdk.Client] = None
        self._project: Optional[label_studio_sdk.Project] = None

        if self.labels is None:
            self.labels = []

    @property
    def ls_client(self) -> label_studio_sdk.Client:
        if self._ls_client is None:
            self._ls_client = label_studio_sdk.Client(
                url=self.ls_url,
                api_key=self.api_key if isinstance(self.api_key, str) else None,
                credentials=self.api_key if isinstance(self.api_key, tuple) else None,
            )
        return self._ls_client

    @property
    def project(self) -> label_studio_sdk.Project:
        """
        При первом использовании ищет проект в LS по индентификатору,
        если его нет -- автоматически создаётся проект с нуля.
        """
        if self._project is not None:
            return self._project
        assert self.ls_client.check_connection(), "No connection to LS."
        _project = (
            self.project_identifier
            if str(self.project_identifier).isnumeric()
            else get_project_by_title(self.ls_client, str(self.project_identifier))
        )
        if _project is None:
            self._project = self.ls_client.start_project(
                title=self.project_identifier,
                description=self.project_description_at_create,
                label_config=self.project_label_config_at_create,
                expert_instruction="",
                show_instruction=False,
                show_skip_button=False,
                enable_empty_annotation=True,
                show_annotation_history=False,
                organization=1,
                color="#FFFFFF",
                maximum_annotations=1,
                is_published=False,
                model_version="",
                is_draft=False,
                min_annotations_to_start_training=10,
                show_collab_predictions=True,
                sampling="Sequential sampling",
                show_ground_truth_first=True,
                show_overlap_first=True,
                overlap_cohort_percentage=100,
                task_data_login=None,
                task_data_password=None,
                control_weights={},
            )
        else:
            assert isinstance(_project, label_studio_sdk.Project)
            self._project = _project

        return self._project

    def _delete_task_from_project(self, task_id: Any) -> None:
        response = self.project.session.request(
            method="DELETE",
            url=self.project.get_url(f"api/tasks/{task_id}/"),
            headers=self.project.headers,
            cookies=self.project.cookies,
        )
        if response.status_code not in [
            204,
            404,
            500,  # Hack for strange behavior in production
            # [2023-02-05 20:15:39,105] [core.utils.common::custom_exception_handler::82] [ERROR] 5c208521-949c-4d43-ac1d-9a19cd3bfaaf Task matching query does not exist.
            # Traceback (most recent call last):
            #   File "/usr/local/lib/python3.8/dist-packages/rest_framework/views.py", line 506, in dispatch
            #     response = handler(request, *args, **kwargs)
            #   File "/usr/local/lib/python3.8/dist-packages/django/utils/decorators.py", line 43, in _wrapper
            #     return bound_method(*args, **kwargs)
            #   File "/label-studio/label_studio/webhooks/utils.py", line 155, in wrap
            #     instance = self.get_object()
            #   File "/usr/local/lib/python3.8/dist-packages/rest_framework/generics.py", line 83, in get_object
            #     queryset = self.filter_queryset(self.get_queryset())
            #   File "/label-studio/label_studio/tasks/api.py", line 196, in get_queryset
            #     project = Task.objects.get(id=self.request.parser_context['kwargs'].get('pk')).project.id
            #   File "/usr/local/lib/python3.8/dist-packages/django/db/models/manager.py", line 85, in manager_method
            #     return getattr(self.get_queryset(), name)(*args, **kwargs)
            #   File "/usr/local/lib/python3.8/dist-packages/django/db/models/query.py", line 429, in get
            #     raise self.model.DoesNotExist(
            # tasks.models.Task.DoesNotExist: Task matching query does not exist.
        ]:
            response.raise_for_status()

    def _convert_data_if_need(self, value: Any):
        if isinstance(value, np.int64):
            return int(value)
        return value

    def build_compute(
        self, ds: DataStore, catalog: Catalog
    ) -> List[ComputeStep]:
        input_dt = catalog.get_datatable(ds, self.input)
        input_uploader_dt = ds.get_or_create_table(
            f"{self.input}_upload",
            TableStoreDB(
                dbconn=self.dbconn,
                name=f"{self.input}_upload",
                data_sql_schema=self.data_sql_schema_primary
                + [Column("task_id", Integer)],
                create_table=self.create_table,
            ),
        )
        catalog.add_datatable(
            f"{self.input}_upload", Table(input_uploader_dt.table_store)
        )
        sync_datetime_dt = ds.get_or_create_table(
            self.sync_table,
            TableStoreDB(
                dbconn=self.dbconn,
                name=self.sync_table,
                data_sql_schema=[
                    Column("project_id", Integer, primary_key=True),
                    Column("last_updated_at", DateTime),
                ],
                create_table=self.create_table,
            ),
        )
        catalog.add_datatable(self.sync_table, Table(sync_datetime_dt.table_store))
        output_dt = ds.get_or_create_table(
            self.output,
            TableStoreDB(
                dbconn=self.dbconn,
                name=self.output,
                data_sql_schema=self.data_sql_schema_primary
                + [Column("annotations", JSON)],
                create_table=self.create_table,
            ),
        )
        catalog.add_datatable(self.output, Table(output_dt.table_store))

        def upload_tasks(df: pd.DataFrame, idx: IndexDF) -> pd.DataFrame:
            """
            Добавляет в LS новые задачи с заданными ключами.
            (Не поддерживает удаление задач, если в input они пропадают)
            """
            if df.empty and idx.empty:
                return pd.DataFrame(columns=self.primary_keys + ["task_id"])

            idx = data_to_index(idx, self.primary_keys)
            if self.delete_unannotated_tasks_only_on_update:
                df_idx = data_to_index(df, self.primary_keys)
                df_existing_tasks = input_uploader_dt.get_data(idx=idx)
                df_existing_tasks_with_output = pd.merge(
                    df_existing_tasks, output_dt.get_data(idx=idx), how="left"
                )
                deleted_idx = index_difference(df_idx, idx)
                if len(df_existing_tasks_with_output) > 0:
                    have_annotations = df_existing_tasks_with_output[
                        "annotations"
                    ].apply(lambda ann: len(ann) > 0 and bool(pd.notna(ann).any())) 
                    df_existing_tasks_to_be_stayed = df_existing_tasks_with_output[
                        have_annotations
                    ]
                    df_existing_tasks_to_be_deleted = pd.merge(
                        df_existing_tasks_with_output[~have_annotations],
                        deleted_idx,
                        how="outer",
                    )
                else:
                    df_existing_tasks_to_be_stayed = pd.DataFrame(
                        columns=self.primary_keys + ["task_id"]
                    )
                    df_existing_tasks_to_be_deleted = pd.merge(
                        pd.DataFrame(columns=self.primary_keys + ["task_id"]),
                        deleted_idx,
                        how="outer",
                    )
                df_to_be_uploaded = pd.concat(
                    [
                        pd.merge(
                            df, df_existing_tasks_to_be_deleted, on=self.primary_keys
                        ),
                        index_to_data(
                            df,
                            index_difference(
                                index_difference(
                                    df_idx,
                                    data_to_index(
                                        df_existing_tasks_to_be_stayed,
                                        self.primary_keys,
                                    ),
                                ),
                                data_to_index(
                                    df_existing_tasks_to_be_deleted, self.primary_keys
                                ),
                            ),
                        ),
                    ],
                    ignore_index=True,
                )
            else:
                df_existing_tasks_to_be_deleted = input_uploader_dt.get_data(idx=idx)
                df_to_be_uploaded = df

            if len(df_existing_tasks_to_be_deleted) > 0:
                for task_id in df_existing_tasks_to_be_deleted["task_id"]:
                    self._delete_task_from_project(task_id)
                output_dt.delete_by_idx(
                    idx=data_to_index(
                        df_existing_tasks_to_be_deleted, self.primary_keys
                    )
                )

            if df.empty and not self.delete_unannotated_tasks_only_on_update:
                return pd.DataFrame(columns=self.primary_keys + ["task_id"])

            if len(df_to_be_uploaded) > 0:
                data_to_be_added = [
                    {
                        "data": {
                            **{
                                primary_key: self._convert_data_if_need(
                                    df_to_be_uploaded.loc[idx, primary_key]
                                )
                                for primary_key in self.primary_keys + self.data_columns
                            }
                        }
                    }
                    for idx in df_to_be_uploaded.index
                ]
                tasks_added = self.project.import_tasks(tasks=data_to_be_added)
                df_to_be_uploaded["task_id"] = tasks_added

            if self.delete_unannotated_tasks_only_on_update:
                df_res = pd.concat(
                    [df_existing_tasks_to_be_stayed, df_to_be_uploaded],
                    ignore_index=True,
                )
            else:
                df_res = df_to_be_uploaded
            logger.debug(
                f"Deleted {len(df_existing_tasks_to_be_deleted)} tasks, uploaded {len(df_to_be_uploaded)} tasks."
            )
            return df_res[self.primary_keys + ["task_id"]]

        def get_annotations_from_ls(
            ds: DataStore,
            input_dts: List[DataTable],
            output_dts: List[DataTable],
            run_config: RunConfig,
            kwargs: Dict[str, Any],
        ) -> None:
            """
            Записывает в табличку задачи из сервера LS вместе с разметкой согласно
            дате последней синхронизации
            """

            # created_ago - очень плохой параметр, он меняется каждый раз, когда происходит запрос
            def _cleanup(values):
                for ann in values:
                    if "created_ago" in ann:
                        del ann["created_ago"]
                return values

            sync_datetime_df = sync_datetime_dt.get_data(
                idx=cast(IndexDF, pd.DataFrame({"project_id": [self.project.id]}))
            )

            if sync_datetime_df.empty:
                sync_datetime_df.loc[0, "project_id"] = self.project.id
                sync_datetime_df.loc[0, "last_updated_at"] = datetime.fromtimestamp(
                    0, tz=timezone.utc
                )

            last_sync = sync_datetime_df.loc[0, "last_updated_at"]

            filters = Filters.create(
                conjunction="and",
                items=[
                    Filters.item(
                        name="tasks:updated_at",  # в sdk нету Column_LS.updated_at
                        operator=Operator.GREATER,
                        column_type=Type.Datetime,
                        value=Filters.value(value=Filters.datetime(last_sync)),
                    )
                ],
            )
            updated_ats = []
            for tasks_page in get_tasks_iter(self.project, filters=filters):
                updated_ats.extend(
                    [
                        datetime.strptime(task["updated_at"], DATETIME_FORMAT)
                        for task in tasks_page
                    ]
                )
                output_df = pd.DataFrame.from_records(
                    {
                        **{
                            primary_key: [
                                task["data"][primary_key] for task in tasks_page
                            ]
                            for primary_key in self.primary_keys
                        },
                        "annotations": [
                            _cleanup(task["annotations"]) for task in tasks_page
                        ],
                    }
                )
                # Удаление возможных дубликатов из LabelStudio.
                output_df = output_df.drop_duplicates(subset=self.primary_keys, keep="last")
                output_dts[0].store_chunk(output_df)

            if len(updated_ats) > 0:
                sync_datetime_df.loc[0, "last_updated_at"] = max(updated_ats)
                sync_datetime_dt.store_chunk(sync_datetime_df)

        return [
            BatchTransformStep(
                ds=ds,
                name=f"{self.name_prefix}upload_data_to_ls",
                labels=[("stage", "upload_data_to_ls"), *(self.labels or [])],
                func=upload_tasks,
                input_dts=[input_dt],
                output_dts=[input_uploader_dt],
                chunk_size=100,
            ),
            DatatableTransformStep(
                name=f"{self.name_prefix}get_annotations_from_ls",
                labels=self.labels,
                func=get_annotations_from_ls,  # type: ignore
                input_dts=[],
                output_dts=[output_dt],
                check_for_changes=False,
            ),
        ]
