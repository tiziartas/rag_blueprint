from typing import Type

from core import Factory
from extraction.datasources.bundestag.configuration import (
    BundestagMineDatasourceConfiguration,
)
from extraction.datasources.bundestag.parser import (
    BundestagMineDatasourceParserFactory,
)
from extraction.datasources.bundestag.reader import (
    BundestagMineDatasourceReaderFactory,
)
from extraction.datasources.core.manager import BasicDatasourceManager


class BundestagMineDatasourceManagerFactory(Factory):
    """Factory for creating datasource managers.

    Provides type-safe creation of datasource managers based on configuration.

    Attributes:
        _configuration_class: Type of configuration object
    """

    _configuration_class: Type = BundestagMineDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: BundestagMineDatasourceConfiguration
    ) -> BasicDatasourceManager:
        """Create an instance of the PDF datasource manager.

        This method constructs a BasicDatasourceManager by creating the appropriate
        reader and parser based on the provided configuration.

        Args:
            configuration: Configuration specifying how to set up the PDF datasource
                          manager, reader, and parser.

        Returns:
            A configured BasicDatasourceManager instance for handling PDF documents.
        """
        reader = BundestagMineDatasourceReaderFactory.create(configuration)
        parser = BundestagMineDatasourceParserFactory.create(configuration)
        return BasicDatasourceManager(
            configuration=configuration,
            reader=reader,
            parser=parser,
        )
