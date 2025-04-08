from typing import Type

from chromadb import HttpClient as ChromaHttpClient
from chromadb.api import ClientAPI as ChromaClient

from core.base_factory import SingletonFactory
from embedding.vector_stores.chroma.configuration import (
    ChromaVectorStoreConfiguration,
)


class ChromaVectorStoreClientFactory(SingletonFactory):
    """
    Factory for creating and managing Chroma vector store client instances.

    This factory implements the Singleton pattern, ensuring only one client
    instance exists per unique configuration. It creates HTTP clients for
    connecting to Chroma DB vector store services.
    """

    _configuration_class: Type = ChromaVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: ChromaVectorStoreConfiguration
    ) -> ChromaClient:
        """
        Create a new Chroma client instance based on the provided configuration.

        Args:
            configuration (ChromaVectorStoreConfiguration): Configuration containing
                connection details for the Chroma vector store.

        Returns:
            ChromaClient: An HTTP client connected to the specified Chroma service.
        """
        return ChromaHttpClient(
            host=configuration.host,
            port=configuration.port,
        )
