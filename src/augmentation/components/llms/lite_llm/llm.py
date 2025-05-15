from typing import Type

from llama_index.llms.litellm import LiteLLM

from augmentation.components.llms.lite_llm.configuration import (
    LiteLLMConfiguration,
)
from core import SingletonFactory


class LiteLLMFactory(SingletonFactory):
    """
    Factory class for creating LiteLLM language model instances.

    This class implements the Singleton pattern to ensure only one instance
    of an LiteLLM model with a specific configuration exists in the application.
    It uses LiteLLMConfiguration to configure the model parameters.

    Attributes:
        _configuration_class: Type of the configuration class used for
            creating LiteLLM model instances.
    """

    _configuration_class: Type = LiteLLMConfiguration

    @classmethod
    def _create_instance(cls, configuration: LiteLLMConfiguration) -> LiteLLM:
        """
        Creates a new instance of the LiteLLM language model.

        Args:
            configuration (LiteLLMConfiguration): Configuration object containing
                settings for the LiteLLM model, including API key, model name,
                maximum tokens, and retry settings.

        Returns:
            LiteLLM: An instance of the LiteLLM language model configured with the
                provided settings.
        """
        api_key = (
            configuration.secrets.api_key.get_secret_value()
            if configuration.secrets.api_key
            else None
        )
        return LiteLLM(
            api_key=api_key,
            api_base=configuration.api_base,
            model=configuration.name,
            max_tokens=configuration.max_tokens,
            max_retries=configuration.max_retries,
        )
