from typing import Type

from llama_index.vector_stores.chroma import ChromaVectorStore

from core.base_factory import SingletonFactory
from embedding.vector_stores.chroma.configuration import (
    ChromaVectorStoreConfiguration,
)


class ChromaVectorStoreFactory(SingletonFactory):
    """Factory for creating configured Chroma vector stores.

    This singleton factory creates and manages ChromaVectorStore instances
    based on the provided configuration. It ensures that only one instance
    is created for each unique configuration.
    """

    _configuration_class: Type = ChromaVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: ChromaVectorStoreConfiguration
    ) -> ChromaVectorStore:
        """Creates a Chroma vector store based on provided configuration.

        Args:
            configuration: Chroma vector store connection configuration
                containing host, port, and collection name.

        Returns:
            ChromaVectorStore: Configured Chroma vector store instance.
        """
        return ChromaVectorStore(
            host=configuration.host,
            port=str(configuration.port),
            collection_name=configuration.collection_name,
        )
