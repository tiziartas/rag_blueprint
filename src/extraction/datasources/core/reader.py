from abc import ABC, abstractmethod
from typing import Any, AsyncIterator


class BaseReader(ABC):
    """Abstract base class for document source readers.

    Defines interface for document extraction from various sources.
    Supports both synchronous and asynchronous implementations through
    generic typing for document types.

    Attributes:
        None
    """

    @abstractmethod
    async def read_all_async(self) -> AsyncIterator[Any]:
        """Asynchronously retrieve all documents from source.

        Returns:
            List[Any]: Collection of extracted documents

        Raises:
            NotImplementedError: Must be implemented by concrete classes
        """
        pass
