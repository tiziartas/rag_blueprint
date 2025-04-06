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
        """
        Valiuate the Qdrant vector store settings.
        """
        self.validate_collection()

    def validate_collection(self) -> None:
        """Validate Qdrant collection existence.

        Raises:
            CollectionExistsException: If collection already exists
        """
        collection_name = self.configuration.collection_name
        if self.client.collection_exists(collection_name):
            raise CollectionExistsException(collection_name)


class QdrantVectorStoreValidatorFactory(SingletonFactory):
    """Factory for creating configured Qdrant clients."""

    _configuration_class: Type = QDrantVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: QDrantVectorStoreConfiguration
    ) -> QdrantClient:
        """Creates a Qdrant client based on provided configuration.

        Args:
            configuration: QDrant connection configuration.

        Returns:
            QdrantClient: Configured client instance.
        """
        client = QdrantClientFactory.create(configuration)
        return QdrantVectorStoreValidator(
            configuration=configuration, client=client
        )
