from typing import AsyncIterator

from core.base_factory import Factory
from extraction.datasources.core.manager import BaseDatasourceManager
from extraction.datasources.notion.cleaner import (
    NotionDatasourceCleaner,
    NotionDatasourceCleanerFactory,
)
from extraction.datasources.notion.configuration import (
    NotionDatasourceConfiguration,
)
from extraction.datasources.notion.document import NotionDocument
from extraction.datasources.notion.parser import (
    NotionDatasourceParser,
    NotionDatasourceParserFactory,
)
from extraction.datasources.notion.reader import (
    NotionDatasourceReader,
    NotionDatasourceReaderFactory,
)


class NotionDatasourceManager(BaseDatasourceManager[NotionDocument]):

    def __init__(
        self,
        configuration: NotionDatasourceConfiguration,
        reader: NotionDatasourceReader,
        parser: NotionDatasourceParser,
        cleaner: NotionDatasourceCleaner,
    ):
        self.configuration = configuration
        self.reader = reader
        self.parser = parser
        self.cleaner = cleaner

    def incremental_sync(self):
        """Update vector storage with current embeddings.

        Raises:
            NotImplementedError: Method must be implemented by subclasses
        """
        raise NotImplementedError("Currently unsupported feature.")

    async def full_refresh_sync(
        self,
    ) -> AsyncIterator[NotionDocument]:
        objects = await self.reader.read_all_async()
        for object in objects:
            document = self.parser.parse(object)
            cleaned_document = self.cleaner.clean(document)
            if cleaned_document:
                yield cleaned_document


class NotionDatasourceManagerFactory(Factory):
    """Factory for creating NotionDatasourceManager instances.

    This factory is responsible for creating instances of the
    NotionDatasourceManager class, which manages the extraction and
    processing of content from Notion databases and pages.
    """

    _configuration_class = NotionDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls,
        configuration: NotionDatasourceConfiguration,
    ) -> NotionDatasourceManager:
        reader = NotionDatasourceReaderFactory.create(configuration)
        parser = NotionDatasourceParserFactory.create(configuration)
        cleaner = NotionDatasourceCleanerFactory.create(configuration)
        return NotionDatasourceManager(
            configuration=configuration,
            reader=reader,
            parser=parser,
            cleaner=cleaner,
        )
