from extraction.bootstrap.configuration.datasources import (
    DatasourceConfigurationRegistry,
    DatasourceName,
)
from extraction.datasources.confluence.configuration import (
    ConfluenceDatasourceConfiguration,
)
from extraction.datasources.confluence.manager import (
    ConfluenceDatasourceManagerFactory,
)
from extraction.datasources.registry import DatasourceManagerRegistry


def register() -> None:
    """
    Registers Confluence datasource components with the application registries.

    This function adds the Confluence datasource manager factory to the DatasourceManagerRegistry
    and registers the Confluence configuration class with the DatasourceConfigurationRegistry.
    Both registrations use the CONFLUENCE datasource name as the key.
    """
    DatasourceManagerRegistry.register(
        DatasourceName.CONFLUENCE, ConfluenceDatasourceManagerFactory
    )
    DatasourceConfigurationRegistry.register(
        DatasourceName.CONFLUENCE, ConfluenceDatasourceConfiguration
    )
