from abc import ABC, abstractmethod
from typing import Generic, List

from extraction.datasources.core.document import DocType


class BaseSplitter(ABC, Generic[DocType]):

    @abstractmethod
    def split(self, document: DocType) -> List[DocType]:
        pass


class BasicMarkdownSplitter(BaseSplitter, Generic[DocType]):

    def split(self, document: DocType) -> List[DocType]:
        return [document]
