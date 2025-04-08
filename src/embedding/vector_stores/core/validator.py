from abc import ABC, abstractmethod


class BaseVectorStoreValidator(ABC):
    """
    Abstract base class for vector store validators.

    This class defines the interface for vector store validators which are
    responsible for verifying that vector store configurations are valid
    before attempting operations.

    All vector store validator implementations should inherit from this class
    and implement the validate method.
    """

    @abstractmethod
    def validate(self) -> None:
        """
        Validate the vector store settings.

        This method should check if all required settings are provided
        and have valid values. It should also verify any connections
        or permissions required for the vector store operation.

        Raises:
            Exception: If validation fails, implementations should raise
                       appropriate exceptions with descriptive messages.
        """
        pass
