from typing import Literal

from pydantic import Field

from embedding.bootstrap.configuration.embedding_model_configuration import (
    EmbeddingModelConfiguration,
    EmbeddingModelProviderName,
)


class HuggingFaceEmbeddingModelConfiguration(EmbeddingModelConfiguration):
    provider: Literal[EmbeddingModelProviderName.HUGGING_FACE] = Field(
        ..., description="The provider of the embedding model."
    )
