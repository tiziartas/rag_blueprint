from typing import Literal, Union

from pydantic import ConfigDict, Field, SecretStr

from core.base_configuration import BaseSecrets
from extraction.bootstrap.configuration.datasources import (
    DatasourceConfiguration,
    DatasourceName,
)


class ConfluenceDatasourceConfiguration(DatasourceConfiguration):
    class Secrets(BaseSecrets):
        model_config = ConfigDict(
            env_file_encoding="utf-8",
            env_prefix="RAG__DATASOURCES__CONFLUENCE__",
            env_nested_delimiter="__",
            extra="ignore",
        )

        username: SecretStr = Field(
            ...,
            description="The username for the confluence data source",
        )
        password: SecretStr = Field(
            ...,
            description="The password for the confluence data source",
        )

    host: str = Field(
        "127.0.0.1", description="Host of the vector store server"
    )
    protocol: Union[Literal["http"], Literal["https"]] = Field(
        "http", description="The protocol for the vector store."
    )
    name: Literal[DatasourceName.CONFLUENCE] = Field(
        ..., description="The name of the data source."
    )
    secrets: Secrets = Field(
        None, description="The secrets for the data source."
    )

    @property
    def base_url(self) -> str:
        return f"{self.protocol}://{self.host}"
