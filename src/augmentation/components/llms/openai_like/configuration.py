from typing import Literal

from pydantic import ConfigDict, Field, SecretStr

from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMConfiguration,
    LLMProviderName,
)
from core.base_configuration import BaseSecrets


class OpenAILikeLLMConfiguration(LLMConfiguration):
    """
    Configuration for OpenAI-compatible language model providers.

    This class defines the configuration settings needed to interact with APIs
    that follow OpenAI's API patterns, including authentication and context
    window settings.
    """

    class Secrets(BaseSecrets):
        """
        Secret configuration values required for authentication with OpenAI-like APIs.

        This class stores sensitive information needed to connect to the API
        and supports loading values from environment variables.
        """

        model_config = ConfigDict(
            env_file_encoding="utf-8",
            env_prefix="RAG__LLMS__OPENAI_LIKE__",
            env_nested_delimiter="__",
            extra="ignore",
        )

        api_key: SecretStr = Field(
            ..., description="API key for the model provider."
        )
        api_base: SecretStr = Field(
            ..., description="Base URL of the model provider."
        )

    provider: Literal[LLMProviderName.OPENAI_LIKE] = Field(
        ..., description="The name of the language model provider."
    )
    secrets: Secrets = Field(
        None, description="The secrets for the language model."
    )
    context_window: int = Field(
        ..., description="The context window size for the language model."
    )
