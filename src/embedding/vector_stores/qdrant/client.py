from typing import Type

from qdrant_client import QdrantClient

from core.base_factory import SingletonFactory
from embedding.vector_stores.qdrant.configuration import (
    QDrantVectorStoreConfiguration,
)


class QdrantClientFactory(SingletonFactory):
    """
    Singleton factory for creating and managing Qdrant client instances.

    This factory ensures that only one Qdrant client instance is created
    for each unique configuration, promoting resource efficiency.
    """

    _configuration_class: Type = QDrantVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: QDrantVectorStoreConfiguration
    ) -> QdrantClient:
        """
        Create a new QdrantClient instance based on the provided configuration.

        Args:
            configuration (QDrantVectorStoreConfiguration): Configuration containing
                connection parameters for the Qdrant server.

        Returns:
            QdrantClient: A configured client instance for interacting with the Qdrant vector database.
        """
        return QdrantClient(
            url=configuration.url,
            port=configuration.port,
            check_compatibility=False,
        )
