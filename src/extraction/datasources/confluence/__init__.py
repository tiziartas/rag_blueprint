# Needed for package discovery
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
    DatasourceManagerRegistry.register(
        DatasourceName.CONFLUENCE, ConfluenceDatasourceManagerFactory
    )
    DatasourceConfigurationRegistry.register(
        DatasourceName.CONFLUENCE, ConfluenceDatasourceConfiguration
    )
