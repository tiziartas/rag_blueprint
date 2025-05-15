from typing import Any, Literal, Optional

from pydantic import ConfigDict, Field, SecretStr

from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMConfiguration,
    LLMProviderName,
)
from core.base_configuration import BaseSecrets


class LiteLLMConfiguration(LLMConfiguration):
    """Configuration for LiteLLM language models, which expose multiple providers.
    To check available providers visit https://docs.litellm.ai/docs/providers.

    This class extends the base LLMConfiguration to provide LiteLLM-specific
    configuration options and secrets management.
    """

    class Secrets(BaseSecrets):
        """Secrets configuration for LiteLLM API authentication.

        Contains sensitive information required to authenticate with the LiteLLM API.
        Environment prefix `env_prefix` has to be provided by parent model, so it includes
        model name.
        """

        model_config = ConfigDict(
            env_file_encoding="utf-8",
            env_nested_delimiter="__",
            extra="ignore",
        )

        api_key: SecretStr = Field(
            ...,
            description="API key for the model provider.",
        )

    provider: Literal[LLMProviderName.LITE_LLM] = Field(
        ..., description="The name of the language model provider."
    )
    api_base: Optional[str] = Field(
        None,
        description="Base URL for the API endpoint of the language model provider. If not provided, api_base is determined by LiteLLM.",
    )
    secrets: Secrets = Field(
        None, description="The secrets for the language model."
    )

    def model_post_init(self, context: Any) -> None:
        """Before loading the secrets, its model config's `env_prefix` has to be set to corresponding model.

        Args:
            context (Any): The context passed to the pydantic model, must contain 'secrets_file' key.
        """
        secrets_class = type(self).model_fields["secrets"].annotation
        secrets_class.model_config["env_prefix"] = (
            self._get_secrets_env_prefix()
        )
        super().model_post_init(context)

    def _get_secrets_env_prefix(self) -> str:
        """Returns the environment variable prefix for the secrets.
        It uses the model name to create a unique prefix for the secrets.
        All non-alphanumeric characters in model name are replaced with underscores.

        The prefix is used to load secrets from environment variables.

        Returns:
            str: The environment variable prefix for the secrets.
        """
        model_name = self.name.upper()
        model_name = "".join(
            char if char.isalnum() else "_" for char in model_name
        )
        return f"RAG__LLMS__{model_name}__"
