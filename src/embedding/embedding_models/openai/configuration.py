from typing import Literal

from pydantic import ConfigDict, Field, SecretStr

from core.base_configuration import BaseSecrets
from embedding.bootstrap.configuration.embedding_model_configuration import (
    EmbeddingModelConfiguration,
    EmbeddingModelProviderName,
)


class OpenAIEmbeddingModelConfiguration(EmbeddingModelConfiguration):
    """
    Configuration for OpenAI embedding models.

    This class defines the configuration parameters needed to use OpenAI
    embedding models, including API credentials, model parameters, and
    request size limitations.
    """

    class Secrets(BaseSecrets):
        """
        Secrets configuration for OpenAI embedding models.

        Contains sensitive credentials required for API authentication with
        appropriate environment variable mappings.
        """

        model_config = ConfigDict(
            env_file_encoding="utf-8",
            env_prefix="RAGKB__EMBEDDING_MODELS__OPEN_AI__",
            env_nested_delimiter="__",
            extra="ignore",
        )

        api_key: SecretStr = Field(..., description="API key for the model")

    provider: Literal[EmbeddingModelProviderName.OPENAI] = Field(
        ..., description="The provider of the embedding model."
    )
    max_request_size_in_tokens: int = Field(
        8191,
        description="Maximum size of the request in tokens.",
    )
    secrets: Secrets = Field(
        None, description="The secrets for the language model."
    )

    def model_post_init(self, __context: dict):
        """
        Post-initialization processing for the model configuration.

        Calculates the appropriate batch size based on the maximum request size
        and the configured text splitter's chunk size if a splitter is defined.

        Args:
            __context: Context information provided by Pydantic during initialization
        """
        super().model_post_init(__context)
        if self.splitter:
            self.batch_size = (
                self.max_request_size_in_tokens
                // self.splitter.chunk_size_in_tokens
            )
