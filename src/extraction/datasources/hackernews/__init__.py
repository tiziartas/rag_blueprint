from extraction.bootstrap.configuration.datasources import (
    DatasourceConfigurationRegistry,
    DatasourceName,
)
from extraction.datasources.hackernews.configuration import (
    HackerNewsDatasourceConfiguration,
)
from extraction.datasources.hackernews.manager import (
    HackerNewsDatasourceManagerFactory,
)
from extraction.datasources.registry import DatasourceManagerRegistry


def register() -> None:
    """
    Registers Hacker News datasource components with the system.

    This function performs following registrations:
    1. Registers the Hacker News datasource configuration with the DatasourceConfigurationRegistry
    2. Registers the Hacker News datasource manager factory with the DatasourceManagerRegistry

    Both registrations use DatasourceName.HackerNews as the identifier.
    """
    DatasourceConfigurationRegistry.register(
        DatasourceName.HACKERNEWS, HackerNewsDatasourceConfiguration
    )
    DatasourceManagerRegistry.register(
        DatasourceName.HACKERNEWS, HackerNewsDatasourceManagerFactory
    )
