from typing import Type

from core import Factory
from extraction.datasources.core.manager import BasicDatasourceManager
from extraction.datasources.pdf.configuration import PDFDatasourceConfiguration
from extraction.datasources.pdf.parser import PDFDatasourceParserFactory
from extraction.datasources.pdf.reader import PDFDatasourceReaderFactory


class PDFDatasourceManagerFactory(Factory):
    """Factory for creating datasource managers.

    Provides type-safe creation of datasource managers based on configuration.

    Attributes:
        _configuration_class: Type of configuration object
    """

    _configuration_class: Type = PDFDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: PDFDatasourceConfiguration
    ) -> BasicDatasourceManager:
        """Create datasource manager instance.

        Args:
            configuration: ExtractionConfiguration object for datasource manager

        Returns:
            BasicDatasourceManager: Datasource manager instance
        """
        reader = PDFDatasourceReaderFactory.create(configuration)
        parser = PDFDatasourceParserFactory.create(configuration)
        return BasicDatasourceManager(configuration, reader, parser)
