from abc import ABC, abstractmethod
from typing import AsyncIterator, Generic

from extraction.bootstrap.configuration.configuration import (
    ExtractionConfiguration,
)
from extraction.datasources.core.cleaner import (
    BaseCleaner,
    BasicMarkdownCleaner,
)
from extraction.datasources.core.document import DocType
from extraction.datasources.core.parser import BaseParser, BasicMarkdownParser
from extraction.datasources.core.reader import BaseReader
from extraction.datasources.core.splitter import (
    BaseSplitter,
    BasicMarkdownSplitter,
)


class BaseDatasourceManager(ABC, Generic[DocType]):
    """Abstract base class for datasource management.

    Provides interface for content extraction and vector storage updates.

    Attributes:
        configuration: Settings for embedding and processing
        reader: Component for reading source content
        cleaner: Component for cleaning extracted content
        splitter: Component for splitting content into chunks
    """

    def __init__(
        self,
        configuration: ExtractionConfiguration,
        reader: BaseReader,
        parser: BaseParser = BasicMarkdownParser(),
        cleaner: BaseCleaner = BasicMarkdownCleaner(),
        splitter: BaseSplitter = BasicMarkdownSplitter(),
    ):
        """Initialize datasource manager.

        Args:
            configuration: Embedding and processing settings
            reader: Content extraction component
            cleaner: Content cleaning component
            splitter: Content splitting component
        """
        self.configuration = configuration
        self.reader = reader
        self.parser = parser
        self.cleaner = cleaner
        self.splitter = splitter

    @abstractmethod
    async def full_refresh_sync(
        self,
    ) -> AsyncIterator[DocType]:
        """Extract and process content from datasource.

        Returns:
            MD docs
        """
        pass

    @abstractmethod
    def incremental_sync(self):
        """Update vector storage with current embeddings."""
        pass


class BasicDatasourceManager(BaseDatasourceManager, Generic[DocType]):
    """Manager for datasource content processing and embedding.

    Implements content extraction pipeline using configurable components
    for reading, cleaning, splitting and embedding content.
    """

    async def full_refresh_sync(
        self,
    ) -> AsyncIterator[DocType]:
        """Extract and process content from datasource.

        Returns:
            Tuple containing:
                - List of raw documents
                - List of cleaned documents
        """
        objects = self.reader.read_all_async()
        async for object in objects:
            md_document = self.parser.parse(object)
            cleaned_document = self.cleaner.clean(md_document)
            if cleaned_document:
                for split_document in self.splitter.split(cleaned_document):
                    yield split_document

    def incremental_sync(self):
        """Update vector storage with current embeddings.

        Raises:
            NotImplementedError: Method must be implemented by subclasses
        """
        raise NotImplementedError("Currently unsupported feature.")
