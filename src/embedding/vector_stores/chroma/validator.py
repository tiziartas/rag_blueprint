from typing import Type

from chromadb.api import ClientAPI as ChromaClient

from core.base_factory import SingletonFactory
from embedding.vector_stores.chroma.client import ChromaVectorStoreClientFactory
from embedding.vector_stores.chroma.configuration import (
    ChromaVectorStoreConfiguration,
)
from embedding.vector_stores.core.exceptions import CollectionExistsException
from embedding.vector_stores.core.validator import BaseVectorStoreValidator


class ChromaVectorStoreValidator(BaseVectorStoreValidator):
    """Validator for Chroma vector store configuration.

    Validates collection settings and existence for Chroma
    vector store backend.

    Attributes:
        configuration: Settings for vector store
        client: Client for Chroma interactions
    """

    def __init__(
        self,
        configuration: ChromaVectorStoreConfiguration,
        client: ChromaClient,
    ):
        """Initialize validator with configuration and client.

        Args:
            configuration: Chroma vector store settings
            client: Client for Chroma operations
        """
        self.configuration = configuration
        self.client = client

    def validate(self) -> None:
        """
        Valiuate the Chroma vector store settings.
        """
        self.validate_collection()

    def validate_collection(self) -> None:
        """Validate Chroma collection existence.

        Raises:
            CollectionExistsException: If collection already exists
        """
        collection_name = self.configuration.collection_name
        if collection_name in self.client.list_collections():
            raise CollectionExistsException(collection_name)


class ChromaVectorStoreValidatorFactory(SingletonFactory):
    """Factory for creating configured Qdrant clients."""

    _configuration_class: Type = ChromaVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: ChromaVectorStoreConfiguration
    ) -> ChromaVectorStoreValidator:
        """Creates a Qdrant client based on provided configuration.

        Args:
            configuration: QDrant connection configuration.

        Returns:
            QdrantClient: Configured client instance.
        """
        client = ChromaVectorStoreClientFactory.create(configuration)
        return ChromaVectorStoreValidator(
            configuration=configuration, client=client
        )
