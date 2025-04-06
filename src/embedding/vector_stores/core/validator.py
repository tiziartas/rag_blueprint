from abc import ABC, abstractmethod


class BaseVectorStoreValidator(ABC):

    @abstractmethod
    def validate(self) -> None:
        """
        Validate the vector store settings.
        """
        pass
