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
    """
    Register QDrant vector store components with the respective registries.

    This function registers:
    1. QDrantVectorStoreConfiguration with the VectorStoreConfigurationRegistry
    2. QdrantVectorStoreFactory with the VectorStoreRegistry
    3. QdrantVectorStoreValidatorFactory with the VectorStoreValidatorRegistry

    This registration enables the application to create, configure, and validate
    QDrant vector store instances through the common registry interfaces.
    """
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
