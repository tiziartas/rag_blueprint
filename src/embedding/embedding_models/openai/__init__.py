from embedding.bootstrap.configuration.embedding_model_configuration import (
    EmbeddingModelConfigurationRegistry,
    EmbeddingModelProviderName,
)
from embedding.embedding_models.openai.configuration import (
    OpenAIEmbeddingModelConfiguration,
)
from embedding.embedding_models.openai.embedding_model import (
    OpenAIEmbeddingModelFactory,
    OpenAIEmbeddingModelTokenizerFactory,
)
from embedding.embedding_models.registry import (
    EmbeddingModelRegistry,
    EmbeddingModelTokenizerRegistry,
)


def register():
    """
    Register OpenAI embedding model implementations with the appropriate registries.

    This function registers:
    1. OpenAIEmbeddingModelConfiguration with the EmbeddingModelConfigurationRegistry
    2. OpenAIEmbeddingModelFactory with the EmbeddingModelRegistry
    3. OpenAIEmbeddingModelTokenizerFactory with the EmbeddingModelTokenizerRegistry

    These registrations enable the system to create and use OpenAI embedding models
    when the OpenAI provider is specified in configuration.
    """
    EmbeddingModelConfigurationRegistry.register(
        EmbeddingModelProviderName.OPENAI, OpenAIEmbeddingModelConfiguration
    )
    EmbeddingModelRegistry.register(
        EmbeddingModelProviderName.OPENAI, OpenAIEmbeddingModelFactory
    )
    EmbeddingModelTokenizerRegistry.register(
        EmbeddingModelProviderName.OPENAI, OpenAIEmbeddingModelTokenizerFactory
    )
