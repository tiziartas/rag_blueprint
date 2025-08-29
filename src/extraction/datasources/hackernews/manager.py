from typing import Type

from core import Factory
from extraction.datasources.hackernews.configuration import (
    HackerNewsDatasourceConfiguration,
)
from extraction.datasources.hackernews.parser import (
        HackerNewsDatasourceParserFactory,
)
from extraction.datasources.hackernews.reader import (
        HackerNewsDatasourceReaderFactory,
)
from extraction.datasources.core.manager import BasicDatasourceManager


class HackerNewsDatasourceManagerFactory(Factory):
    """Factory for creating datasource managers.

    Provides type-safe creation of datasource managers based on configuration.

    Attributes:
        _configuration_class: Type of configuration object
    """

    _configuration_class: Type = HackerNewsDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: HackerNewsDatasourceConfiguration
    ) -> BasicDatasourceManager:
        """Create an instance of the Hacker News datasource manager.

        This method constructs a BasicDatasourceManager by creating the appropriate
        reader and parser based on the provided configuration.

        Args:
            configuration: Configuration specifying how to set up the Hacker News datasource
                          manager, reader, and parser.

        Returns:
            A configured BasicDatasourceManager instance for handling Hacker News documents.
        """
        reader = HackerNewsDatasourceReaderFactory.create(configuration)
        parser = HackerNewsDatasourceParserFactory.create(configuration)
        return BasicDatasourceManager(
            configuration=configuration,
            reader=reader,
            parser=parser,
        )
