from abc import ABC, abstractmethod
from typing import Generic

from llama_index.core import Document

from extraction.datasources.core.document import DocType


class BaseParser(ABC, Generic[DocType]):
    @abstractmethod
    def parse(self, content: str) -> DocType:
        pass


class BasicMarkdownParser(BaseParser[Document]):

    def parse(self, markdown: str) -> Document:
        return Document(text=markdown, metadata={})
