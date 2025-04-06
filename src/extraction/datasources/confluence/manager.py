from typing import Type

from core import Factory
from extraction.datasources.confluence.configuration import (
    ConfluenceDatasourceConfiguration,
)
from extraction.datasources.confluence.parser import (
    ConfluenceDatasourceParserFactory,
)
from extraction.datasources.confluence.reader import (
    ConfluenceDatasourceReaderFactory,
)
from extraction.datasources.core.manager import BasicDatasourceManager


class ConfluenceDatasourceManagerFactory(Factory):
    """Factory for creating datasource managers.

    Provides type-safe creation of datasource managers based on configuration.

    Attributes:
        _configuration_class: Type of configuration object
    """

    _configuration_class: Type = ConfluenceDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: ConfluenceDatasourceConfiguration
    ) -> BasicDatasourceManager:
        """Create datasource manager instance.

        Args:
            configuration: ExtractionConfiguration object for datasource manager

        Returns:
            BasicDatasourceManager: Datasource manager instance
        """
        reader = ConfluenceDatasourceReaderFactory.create(configuration)
        parser = ConfluenceDatasourceParserFactory.create(configuration)
        return BasicDatasourceManager(configuration, reader, parser)
