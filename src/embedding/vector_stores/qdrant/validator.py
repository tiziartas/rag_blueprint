from typing import Type

from qdrant_client import QdrantClient

from core.base_factory import SingletonFactory
from embedding.vector_stores.core.exceptions import CollectionExistsException
from embedding.vector_stores.core.validator import BaseVectorStoreValidator
from embedding.vector_stores.qdrant.client import QdrantClientFactory
from embedding.vector_stores.qdrant.configuration import (
    QDrantVectorStoreConfiguration,
)


class QdrantVectorStoreValidator(BaseVectorStoreValidator):
    """Validator for Qdrant vector store configuration.

    Validates collection settings and existence for Qdrant
    vector store backend.

    Attributes:
        configuration: Settings for vector store
        client: Client for Qdrant interactions
    """

    def __init__(
        self,
        configuration: QDrantVectorStoreConfiguration,
        client: QdrantClient,
    ):
        """Initialize validator with configuration and client.

        Args:
            configuration: Qdrant vector store settings
            client: Client for Qdrant operations
        """
        self.configuration = configuration
        self.client = client

    def validate(self) -> None:
        """Validate the Qdrant vector store settings.

        Performs validation checks on the provided configuration
        to ensure compatibility with Qdrant backend requirements.
        """
        self.validate_collection()

    def validate_collection(self) -> None:
        """Validate Qdrant collection existence.

        Checks if the specified collection already exists in the Qdrant
        database and raises an exception if it does, preventing
        unintentional overwriting of existing collections.

        Raises:
            CollectionExistsException: If collection already exists
                in the Qdrant database with the specified name
        """
        collection_name = self.configuration.collection_name
        if self.client.collection_exists(collection_name):
            raise CollectionExistsException(collection_name)


class QdrantVectorStoreValidatorFactory(SingletonFactory):
    """Factory for creating Qdrant vector store validators.

    Implements the singleton pattern to ensure only one validator
    instance exists for each unique configuration.
    """

    _configuration_class: Type = QDrantVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: QDrantVectorStoreConfiguration
    ) -> QdrantVectorStoreValidator:
        """Creates a Qdrant validator based on provided configuration.

        Instantiates a new validator with the appropriate client
        for the given configuration.

        Args:
            configuration: QDrant connection configuration.

        Returns:
            QdrantVectorStoreValidator: Configured validator instance.
        """
        client = QdrantClientFactory.create(configuration)
        return QdrantVectorStoreValidator(
            configuration=configuration, client=client
        )
