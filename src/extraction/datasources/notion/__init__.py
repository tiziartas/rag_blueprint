"""
To be rebuild using Airbyte Notion source in the future
"""

from extraction.bootstrap.configuration.datasources import (
    DatasourceConfigurationRegistry,
    DatasourceName,
)
from extraction.datasources.notion.configuration import (
    NotionDatasourceConfiguration,
)
from extraction.datasources.notion.manager import NotionDatasourceManagerFactory
from extraction.datasources.registry import DatasourceManagerRegistry


def register() -> None:
    """
    Registers Notion as a datasource in the application.

    This function connects the Notion datasource to the application by:
    1. Registering the NotionDatasourceConfiguration with the configuration registry
    2. Registering the NotionDatasourceManagerFactory with the manager registry

    Both registrations use the NOTION datasource name as their identifier.
    """
    DatasourceConfigurationRegistry.register(
        DatasourceName.NOTION, NotionDatasourceConfiguration
    )
    DatasourceManagerRegistry.register(
        DatasourceName.NOTION, NotionDatasourceManagerFactory
    )
