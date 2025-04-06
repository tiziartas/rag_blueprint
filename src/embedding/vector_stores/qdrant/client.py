from typing import Type

from qdrant_client import QdrantClient

from core.base_factory import SingletonFactory
from embedding.vector_stores.qdrant.configuration import (
    QDrantVectorStoreConfiguration,
)


class QdrantClientFactory(SingletonFactory):
    _configuration_class: Type = QDrantVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: QDrantVectorStoreConfiguration
    ) -> QdrantClient:
        return QdrantClient(
            url=configuration.url,
            port=configuration.port,
            check_compatibility=False,
        )
