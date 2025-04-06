from abc import ABC, abstractmethod
from typing import Generic

from llama_index.core.schema import TextNode

from extraction.datasources.core.document import DocType


class BaseSplitter(ABC, Generic[DocType]):
    """Abstract base class for document splitter.

    Defines interface for splitter documents into text nodes with
    generic typing support for document types.
    """

    @abstractmethod
    def split(self, document: DocType) -> TextNode:
        """Split documents into text nodes.

        Args:
            documents: Collection of documents to split

        Returns:
            List[TextNode]: Collection of text nodes
        """
        pass
