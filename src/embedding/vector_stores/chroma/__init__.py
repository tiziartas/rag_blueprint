from embedding.bootstrap.configuration.vector_store_configuration import (
    VectorStoreConfigurationRegistry,
    VectorStoreName,
)
from embedding.vector_stores.chroma.configuration import (
    ChromaVectorStoreConfiguration,
)
from embedding.vector_stores.chroma.validator import (
    ChromaVectorStoreValidatorFactory,
)
from embedding.vector_stores.chroma.vector_store import ChromaVectorStoreFactory
from embedding.vector_stores.registry import (
    VectorStoreRegistry,
    VectorStoreValidatorRegistry,
)


def register() -> None:
    """
    Registers Chroma vector store components with the appropriate registries.

    This function performs the following registrations:
    1. ChromaVectorStoreConfiguration with VectorStoreConfigurationRegistry
    2. ChromaVectorStoreFactory with VectorStoreRegistry
    3. ChromaVectorStoreValidatorFactory with VectorStoreValidatorRegistry

    All registrations use VectorStoreName.CHROMA as the identifier.
    """
    VectorStoreConfigurationRegistry.register(
        VectorStoreName.CHROMA,
        ChromaVectorStoreConfiguration,
    )
    VectorStoreRegistry.register(
        VectorStoreName.CHROMA, ChromaVectorStoreFactory
    )
    VectorStoreValidatorRegistry.register(
        VectorStoreName.CHROMA, ChromaVectorStoreValidatorFactory
    )
