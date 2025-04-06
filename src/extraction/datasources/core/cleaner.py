from abc import ABC, abstractmethod
from typing import Generic

from extraction.datasources.core.document import DocType


class BaseCleaner(ABC, Generic[DocType]):
    """Abstract base class defining document cleaning interface.

    Provides interface for cleaning document collections with type safety
    through generic typing.

    Attributes:
        None
    """

    @abstractmethod
    def clean(self, document: DocType) -> DocType:
        """Clean a list of documents.

        Args:
            document: List of documents to clean

        Returns:
            DocType: List of cleaned documents
        """
        pass


class BasicMarkdownCleaner(BaseCleaner, Generic[DocType]):
    """Generic document cleaner implementation.

    Removes empty documents from collections while tracking progress.
    Supports any document type with a text attribute.
    """

    def clean(self, document: DocType) -> DocType:
        """Remove empty documents from collection.

        Args:
            documents: List of documents to clean

        Returns:
            DocType: Filtered list containing only non-empty documents
        """
        if not self._has_empty_content(document):
            return document

        return None

    @staticmethod
    def _has_empty_content(document: DocType) -> bool:
        """Check if document has empty content.

        Args:
            document: Document to check (must have text attribute)

        Returns:
            bool: True if document text is empty after stripping whitespace
        """
        return not document.text.strip()
