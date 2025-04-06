# Needed for package discovery
from extraction.bootstrap.configuration.datasources import (
    DatasourceConfigurationRegistry,
    DatasourceName,
)
from extraction.datasources.pdf.configuration import PDFDatasourceConfiguration
from extraction.datasources.pdf.manager import PDFDatasourceManagerFactory
from extraction.datasources.registry import DatasourceManagerRegistry


def register() -> None:
    DatasourceManagerRegistry.register(
        DatasourceName.PDF, PDFDatasourceManagerFactory
    )
    DatasourceConfigurationRegistry.register(
        DatasourceName.PDF, PDFDatasourceConfiguration
    )
