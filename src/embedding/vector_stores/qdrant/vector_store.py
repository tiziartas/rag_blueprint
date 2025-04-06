from typing import Type

from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient

from core.base_factory import SingletonFactory
from embedding.vector_stores.qdrant.client import QdrantClientFactory
from embedding.vector_stores.qdrant.configuration import (
    QDrantVectorStoreConfiguration,
)


class QdrantVectorStoreFactory(SingletonFactory):
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
        return QdrantVectorStore(
            client=client, collection_name=configuration.collection_name
        )
