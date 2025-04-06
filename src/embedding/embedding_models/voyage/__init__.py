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
from embedding.embedding_models.voyage.voyage import (
    VoyageEmbeddingModelFactory,
    VoyageEmbeddingModelTokenizerFactory,
)


def register():
    EmbeddingModelConfigurationRegistry.register(
        EmbeddingModelProviderName.VOYAGE, VoyageEmbeddingModelConfiguration
    )
    EmbeddingModelRegistry.register(
        EmbeddingModelProviderName.VOYAGE, VoyageEmbeddingModelFactory
    )
    EmbeddingModelTokenizerRegistry.register(
        EmbeddingModelProviderName.VOYAGE, VoyageEmbeddingModelTokenizerFactory
    )
