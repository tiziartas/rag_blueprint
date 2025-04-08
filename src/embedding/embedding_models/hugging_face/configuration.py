from typing import Literal

from pydantic import Field

from embedding.bootstrap.configuration.embedding_model_configuration import (
    EmbeddingModelConfiguration,
    EmbeddingModelProviderName,
)


class HuggingFaceEmbeddingModelConfiguration(EmbeddingModelConfiguration):
    """
    Configuration class for Hugging Face embedding models.

    This class extends the base EmbeddingModelConfiguration to provide
    specific configuration options for Hugging Face embedding models.
    """

    provider: Literal[EmbeddingModelProviderName.HUGGING_FACE] = Field(
        ..., description="The provider of the embedding model."
    )
