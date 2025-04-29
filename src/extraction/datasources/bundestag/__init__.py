from extraction.bootstrap.configuration.datasources import (
    DatasourceConfigurationRegistry,
    DatasourceName,
)
from extraction.datasources.bundestag.configuration import (
    BundestagMineDatasourceConfiguration,
)
from extraction.datasources.bundestag.manager import (
    BundestagMineDatasourceManagerFactory,
)
from extraction.datasources.registry import DatasourceManagerRegistry


def register() -> None:
    """
    Registers Bundestag datasource components with the system.

    This function performs following registrations:
    1. Registers the Bundestag datasource configuration with the DatasourceConfigurationRegistry
    2. Registers the Bundestag datasource manager factory with the DatasourceManagerRegistry

    Both registrations use DatasourceName.Bundestag as the identifier.
    """
    DatasourceConfigurationRegistry.register(
        DatasourceName.BUNDESTAG, BundestagMineDatasourceConfiguration
    )
    DatasourceManagerRegistry.register(
        DatasourceName.BUNDESTAG, BundestagMineDatasourceManagerFactory
    )
