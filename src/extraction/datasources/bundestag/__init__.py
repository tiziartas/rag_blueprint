from extraction.bootstrap.configuration.datasources import (
    DatasourceConfigurationRegistry,
    DatasourceName,
)
from extraction.datasources.bundestag.configuration import (
    BundestagMineDatasourceConfiguration,
)


def register() -> None:
    """
    Registers Bundestag datasource components with the system.

    This function performs following registrations:
    2. Registers the Bundestag datasource configuration with the DatasourceConfigurationRegistry

    Both registrations use DatasourceName.Bundestag as the identifier.
    """
    DatasourceConfigurationRegistry.register(
        DatasourceName.BUNDESTAG, BundestagMineDatasourceConfiguration
    )
