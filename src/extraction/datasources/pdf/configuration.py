from typing import Literal

from pydantic import Field

from extraction.bootstrap.configuration.datasources import (
    DatasourceConfiguration,
    DatasourceName,
)


class PDFDatasourceConfiguration(DatasourceConfiguration):

    name: Literal[DatasourceName.PDF] = Field(
        ..., description="The name of the data source."
    )
    base_path: str = Field(
        ..., description="Base path to the directory containing PDF files"
    )
