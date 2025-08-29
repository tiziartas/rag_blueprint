from typing import Literal

from pydantic import Field

from extraction.bootstrap.configuration.datasources import (
    DatasourceConfiguration,
    DatasourceName,
)


class HackerNewsDatasourceConfiguration(DatasourceConfiguration):
    name: Literal[DatasourceName.HACKERNEWS] = Field(
        ...,
        description="Identifier specifying this configuration is for the Hacker News datasource",
    )

