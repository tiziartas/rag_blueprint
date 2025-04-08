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
            ..., description="Authentication token for accessing the Notion API"
        )

    name: Literal[DatasourceName.NOTION] = Field(
        ..., description="Identifier specifying this as a Notion datasource"
    )
    home_page_database_id: Optional[str] = Field(
        None,
        description="ID of the root Notion database from which pages and child databases will be extracted; extraction is skipped if not provided",
    )
    export_batch_size: int = Field(
        3,
        description="Maximum number of pages to export concurrently; controls throughput vs. rate limit compliance",
    )
    secrets: Secrets = Field(
        None,
        description="Authentication credentials required for connecting to Notion API",
    )
