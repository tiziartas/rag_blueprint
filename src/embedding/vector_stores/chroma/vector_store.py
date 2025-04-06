from typing import Type

from llama_index.vector_stores.chroma import ChromaVectorStore
from qdrant_client import QdrantClient

from core.base_factory import SingletonFactory
from embedding.vector_stores.chroma.configuration import (
    ChromaVectorStoreConfiguration,
)


class ChromaVectorStoreFactory(SingletonFactory):
    """Factory for creating configured Qdrant clients."""

    _configuration_class: Type = ChromaVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: ChromaVectorStoreConfiguration
    ) -> QdrantClient:
        """Creates a Qdrant client based on provided configuration.

        Args:
            configuration: QDrant connection configuration.

        Returns:
            QdrantClient: Configured client instance.
        """
        return ChromaVectorStore(
            host=configuration.host,
            port=str(configuration.port),
            collection_name=configuration.collection_name,
        )
