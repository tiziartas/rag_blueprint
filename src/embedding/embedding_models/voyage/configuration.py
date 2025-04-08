from typing import Literal

from pydantic import ConfigDict, Field, SecretStr

from core.base_configuration import BaseSecrets
from embedding.bootstrap.configuration.embedding_model_configuration import (
    EmbeddingModelConfiguration,
    EmbeddingModelProviderName,
)


class VoyageEmbeddingModelConfiguration(EmbeddingModelConfiguration):
    """Configuration for Voyage embedding models.

    This class represents the configuration needed for using Voyage AI embedding models,
    including authentication credentials and model settings.
    """

    class Secrets(BaseSecrets):
        """Secrets for Voyage embedding model authentication.

        Contains API key and other sensitive information required to authenticate
        with the Voyage AI API for embedding generation.
        """

        model_config = ConfigDict(
            env_file_encoding="utf-8",
            env_prefix="RAGKB__EMBEDDING_MODELS__VOYAGE__",
            env_nested_delimiter="__",
            extra="ignore",
        )

        api_key: SecretStr = Field(..., description="API key for the model")

    provider: Literal[EmbeddingModelProviderName.VOYAGE] = Field(
        ..., description="The provider of the embedding model."
    )
    secrets: Secrets = Field(
        None, description="The secrets for the language model."
    )
