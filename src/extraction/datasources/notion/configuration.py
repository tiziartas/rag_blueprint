from typing import Literal, Optional

from pydantic import ConfigDict, Field, SecretStr

from core.base_configuration import BaseSecrets
from extraction.bootstrap.configuration.datasources import (
    DatasourceConfiguration,
    DatasourceName,
)


class NotionDatasourceConfiguration(DatasourceConfiguration):
    class Secrets(BaseSecrets):
        model_config = ConfigDict(
            env_file_encoding="utf-8",
            env_prefix="RAG__DATASOURCES__NOTION__",
            env_nested_delimiter="__",
            extra="ignore",
        )

        api_token: SecretStr = Field(
            ..., description="The token for the notion data source"
        )

    name: Literal[DatasourceName.NOTION] = Field(
        ..., description="The name of the data source."
    )
    home_page_database_id: Optional[str] = Field(
        None,
        description="Notion home page database id used for extraction of pages and database. If null, this extraction will be skipped.",
    )
    export_batch_size: int = Field(
        3,
        description="Number of pages being exported ansychronously. Decrease to avoid NotionAPI rate limits, smaller batch slows the export down.",
    )
    secrets: Secrets = Field(
        None, description="The secrets for the data source."
    )
