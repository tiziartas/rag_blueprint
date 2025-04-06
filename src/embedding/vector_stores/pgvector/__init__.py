from embedding.bootstrap.configuration.vector_store_configuration import (
    VectorStoreConfigurationRegistry,
    VectorStoreName,
)
from embedding.vector_stores.pgvector.configuration import (
    PGVectorStoreConfiguration,
)
from embedding.vector_stores.pgvector.validator import (
    PGVectorStoreValidatorFactory,
)
from embedding.vector_stores.pgvector.vector_store import PGVectorStoreFactory
from embedding.vector_stores.registry import (
    VectorStoreRegistry,
    VectorStoreValidatorRegistry,
)


def register() -> None:
    VectorStoreConfigurationRegistry.register(
        VectorStoreName.PGVECTOR,
        PGVectorStoreConfiguration,
    )
    VectorStoreRegistry.register(VectorStoreName.PGVECTOR, PGVectorStoreFactory)
    VectorStoreValidatorRegistry.register(
        VectorStoreName.PGVECTOR, PGVectorStoreValidatorFactory
    )
