from extraction.bootstrap.configuration.datasources import (
    DatasourceConfigurationRegistry,
    DatasourceName,
)
from extraction.datasources.pdf.configuration import PDFDatasourceConfiguration
from extraction.datasources.pdf.manager import PDFDatasourceManagerFactory
from extraction.datasources.registry import DatasourceManagerRegistry


def register() -> None:
    """
    Registers PDF datasource components with the system.

    This function performs two registrations:
    1. Registers the PDF datasource manager factory with the DatasourceManagerRegistry
    2. Registers the PDF datasource configuration with the DatasourceConfigurationRegistry

    Both registrations use DatasourceName.PDF as the identifier.
    """
    DatasourceManagerRegistry.register(
        DatasourceName.PDF, PDFDatasourceManagerFactory
    )
    DatasourceConfigurationRegistry.register(
        DatasourceName.PDF, PDFDatasourceConfiguration
    )
