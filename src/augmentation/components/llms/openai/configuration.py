from typing import Literal

from pydantic import ConfigDict, Field, SecretStr

from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMConfiguration,
    LLMProviderName,
)
from core.base_configuration import BaseSecrets


class OpenAILLMConfiguration(LLMConfiguration):
    """Configuration for OpenAI language models.

    This class extends the base LLMConfiguration to provide OpenAI-specific
    configuration options and secrets management.
    """

    class Secrets(BaseSecrets):
        """Secrets configuration for OpenAI API authentication.

        Contains sensitive information required to authenticate with the OpenAI API.
        Values can be provided through environment variables with the prefix RAG__LLMS__OPENAI__.
        """

        model_config = ConfigDict(
            env_file_encoding="utf-8",
            env_prefix="RAG__LLMS__OPENAI__",
            env_nested_delimiter="__",
            extra="ignore",
        )

        api_key: SecretStr = Field(
            ..., description="API key for the model provider."
        )

    provider: Literal[LLMProviderName.OPENAI] = Field(
        ..., description="The name of the language model provider."
    )
    secrets: Secrets = Field(
        None, description="The secrets for the language model."
    )
