from embedding.bootstrap.configuration.embedding_model_configuration import (
    EmbeddingModelConfigurationRegistry,
    EmbeddingModelProviderName,
)
from embedding.embedding_models.openai.configuration import (
    OpenAIEmbeddingModelConfiguration,
)
from embedding.embedding_models.openai.openai import (
    OpenAIEmbeddingModelFactory,
    OpenAIEmbeddingModelTokenizerFactory,
)
from embedding.embedding_models.registry import (
    EmbeddingModelRegistry,
    EmbeddingModelTokenizerRegistry,
)


def register():
    EmbeddingModelConfigurationRegistry.register(
        EmbeddingModelProviderName.OPENAI, OpenAIEmbeddingModelConfiguration
    )
    EmbeddingModelRegistry.register(
        EmbeddingModelProviderName.OPENAI, OpenAIEmbeddingModelFactory
    )
    EmbeddingModelTokenizerRegistry.register(
        EmbeddingModelProviderName.OPENAI, OpenAIEmbeddingModelTokenizerFactory
    )
