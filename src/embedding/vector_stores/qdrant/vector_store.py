from typing import Type

from llama_index.vector_stores.qdrant import QdrantVectorStore

from core.base_factory import SingletonFactory
from embedding.vector_stores.qdrant.client import QdrantClientFactory
from embedding.vector_stores.qdrant.configuration import (
    QDrantVectorStoreConfiguration,
)


class QdrantVectorStoreFactory(SingletonFactory):
    """Factory for creating configured Qdrant vector store instances using the Singleton pattern."""

    _configuration_class: Type = QDrantVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: QDrantVectorStoreConfiguration
    ) -> QdrantVectorStore:
        """Creates a Qdrant vector store based on provided configuration.

        This method instantiates a Qdrant client using the QdrantClientFactory
        and uses it to create a QdrantVectorStore instance with the specified
        collection name from the configuration.

        Args:
            configuration: QDrant connection configuration containing
                           connection parameters and collection name.

        Returns:
            QdrantVectorStore: Configured vector store instance ready for
                              embedding storage and retrieval operations.
        """
        client = QdrantClientFactory.create(configuration)
        return QdrantVectorStore(
            client=client, collection_name=configuration.collection_name
        )
