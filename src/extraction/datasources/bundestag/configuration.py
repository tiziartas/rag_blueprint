from typing import Literal

from pydantic import Field

from extraction.bootstrap.configuration.datasources import (
    DatasourceConfiguration,
    DatasourceName,
)


class BundestagMineDatasourceConfiguration(DatasourceConfiguration):
    name: Literal[DatasourceName.BUNDESTAG] = Field(
        ...,
        description="Identifier specifying this configuration is for the Bundestag datasource",
    )
