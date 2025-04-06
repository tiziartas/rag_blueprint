from embedding.bootstrap.configuration.embedding_model_configuration import (
    EmbeddingModelConfigurationRegistry,
    EmbeddingModelProviderName,
)
from embedding.embedding_models.registry import (
    EmbeddingModelRegistry,
    EmbeddingModelTokenizerRegistry,
)
from embedding.embedding_models.voyage.configuration import (
    VoyageEmbeddingModelConfiguration,
)
from embedding.embedding_models.voyage.embedding_model import (
    VoyageEmbeddingModelFactory,
    VoyageEmbeddingModelTokenizerFactory,
)


def register():
    """
    Registers Voyage embedding model components with the appropriate registries.

    This function performs three registrations:
    1. Registers VoyageEmbeddingModelConfiguration with the configuration registry
    2. Registers VoyageEmbeddingModelFactory with the model registry
    3. Registers VoyageEmbeddingModelTokenizerFactory with the tokenizer registry

    This enables the system to use Voyage embedding models when VOYAGE is specified
    as the embedding model provider.
    """
    EmbeddingModelConfigurationRegistry.register(
        EmbeddingModelProviderName.VOYAGE, VoyageEmbeddingModelConfiguration
    )
    EmbeddingModelRegistry.register(
        EmbeddingModelProviderName.VOYAGE, VoyageEmbeddingModelFactory
    )
    EmbeddingModelTokenizerRegistry.register(
        EmbeddingModelProviderName.VOYAGE, VoyageEmbeddingModelTokenizerFactory
    )
