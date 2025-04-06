from abc import ABC, abstractmethod
from typing import AsyncIterator, List

from extraction.datasources.core.document import BaseDocument
from extraction.datasources.core.manager import BaseDatasourceManager


class BaseDatasourceOrchestrator(ABC):
    """Abstract base class for datasource orchestration.

    Defines interface for managing content extraction, embedding generation,
    and vector storage operations across datasources.

    Note:
        All implementing classes must provide concrete implementations
        of extract, embed, save and update methods.
    """

    def __init__(
        self,
        datasource_managers: List[BaseDatasourceManager],
    ):
        self.datasource_managers = datasource_managers

    @abstractmethod
    async def full_refresh_sync(self) -> AsyncIterator[BaseDocument]:
        """Extract content from configured datasources.

        Performs asynchronous content extraction from all configured
        datasource implementations.
        """
        pass

    @abstractmethod
    async def incremental_sync(self) -> AsyncIterator[BaseDocument]:
        pass
