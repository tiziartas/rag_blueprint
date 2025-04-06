from embedding.bootstrap.configuration.vector_store_configuration import (
    VectorStoreConfigurationRegistry,
    VectorStoreName,
)
from embedding.vector_stores.qdrant.configuration import (
    QDrantVectorStoreConfiguration,
)
from embedding.vector_stores.qdrant.validator import (
    QdrantVectorStoreValidatorFactory,
)
from embedding.vector_stores.qdrant.vector_store import QdrantVectorStoreFactory
from embedding.vector_stores.registry import (
    VectorStoreRegistry,
    VectorStoreValidatorRegistry,
)


def register() -> None:
    VectorStoreConfigurationRegistry.register(
        VectorStoreName.QDRANT,
        QDrantVectorStoreConfiguration,
    )
    VectorStoreRegistry.register(
        VectorStoreName.QDRANT, QdrantVectorStoreFactory
    )
    VectorStoreValidatorRegistry.register(
        VectorStoreName.QDRANT, QdrantVectorStoreValidatorFactory
    )
