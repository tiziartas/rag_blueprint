from embedding.bootstrap.configuration.embedding_model_configuration import (
    EmbeddingModelConfigurationRegistry,
    EmbeddingModelProviderName,
)
from embedding.embedding_models.hugging_face.configuration import (
    HuggingFaceEmbeddingModelConfiguration,
)
from embedding.embedding_models.hugging_face.hugging_face import (
    HuggingFaceEmbeddingModelFactory,
    HuggingFaceEmbeddingModelTokenizerFactory,
)
from embedding.embedding_models.registry import (
    EmbeddingModelRegistry,
    EmbeddingModelTokenizerRegistry,
)


def register():
    EmbeddingModelConfigurationRegistry.register(
        EmbeddingModelProviderName.HUGGING_FACE,
        HuggingFaceEmbeddingModelConfiguration,
    )
    EmbeddingModelRegistry.register(
        EmbeddingModelProviderName.HUGGING_FACE,
        HuggingFaceEmbeddingModelFactory,
    )
    EmbeddingModelTokenizerRegistry.register(
        EmbeddingModelProviderName.HUGGING_FACE,
        HuggingFaceEmbeddingModelTokenizerFactory,
    )
