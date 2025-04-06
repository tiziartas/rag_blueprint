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
    DatasourceConfigurationRegistry.register(
        DatasourceName.NOTION, NotionDatasourceConfiguration
    )
    DatasourceManagerRegistry.register(
        DatasourceName.NOTION, NotionDatasourceManagerFactory
    )
