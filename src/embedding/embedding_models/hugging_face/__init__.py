from embedding.bootstrap.configuration.embedding_model_configuration import (
    EmbeddingModelConfigurationRegistry,
    EmbeddingModelProviderName,
)
from embedding.embedding_models.hugging_face.configuration import (
    HuggingFaceEmbeddingModelConfiguration,
)
from embedding.embedding_models.hugging_face.embedding_model import (
    HuggingFaceEmbeddingModelFactory,
    HuggingFaceEmbeddingModelTokenizerFactory,
)
from embedding.embedding_models.registry import (
    EmbeddingModelRegistry,
    EmbeddingModelTokenizerRegistry,
)


def register():
    """
    Register all components required for HuggingFace embedding models.

    This function registers the HuggingFace-specific implementations with the appropriate registries:
    - Configuration class with the configuration registry
    - Model factory with the embedding model registry
    - Tokenizer factory with the tokenizer registry
    """
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
