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
            description="Username credential used to authenticate with the Confluence instance",
        )
        password: SecretStr = Field(
            ...,
            description="Password credential used to authenticate with the Confluence instance",
        )

    host: str = Field(
        "127.0.0.1",
        description="Hostname or IP address of the Confluence server instance",
    )
    protocol: Union[Literal["http"], Literal["https"]] = Field(
        "http",
        description="Communication protocol used to connect to the Confluence server",
    )
    name: Literal[DatasourceName.CONFLUENCE] = Field(
        ...,
        description="Identifier specifying this configuration is for a Confluence datasource",
    )
    secrets: Secrets = Field(
        None,
        description="Authentication credentials required to access the Confluence instance",
    )

    @property
    def base_url(self) -> str:
        """
        Constructs the complete base URL for the Confluence API from the protocol and host.

        Returns:
            str: The fully formed base URL to the Confluence instance
        """
        return f"{self.protocol}://{self.host}"
