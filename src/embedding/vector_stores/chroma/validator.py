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
    vector store backend. Ensures proper configuration before
    operations are performed against the vector store.
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
        """Validate the Chroma vector store settings.

        Performs all required validation steps for the Chroma vector store,
        including collection validation.

        Raises:
            CollectionExistsException: If collection already exists
        """
        self.validate_collection()

    def validate_collection(self) -> None:
        """Validate Chroma collection existence.

        Checks if a collection with the specified name already exists
        in the Chroma database.

        Raises:
            CollectionExistsException: If collection already exists
        """
        collection_name = self.configuration.collection_name
        if collection_name in self.client.list_collections():
            raise CollectionExistsException(collection_name)


class ChromaVectorStoreValidatorFactory(SingletonFactory):
    """Factory for creating configured Chroma validator instances.

    Manages the creation and caching of ChromaVectorStoreValidator
    instances based on provided configuration.

    Attributes:
        _configuration_class (Type): The configuration class for Chroma vector store.
    """

    _configuration_class: Type = ChromaVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: ChromaVectorStoreConfiguration
    ) -> ChromaVectorStoreValidator:
        """Creates a Chroma validator based on provided configuration.

        Args:
            configuration: Chroma connection configuration.

        Returns:
            ChromaVectorStoreValidator: Configured validator instance.
        """
        client = ChromaVectorStoreClientFactory.create(configuration)
        return ChromaVectorStoreValidator(
            configuration=configuration, client=client
        )
