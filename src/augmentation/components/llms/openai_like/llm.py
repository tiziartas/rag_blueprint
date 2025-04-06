from typing import Type

from llama_index.llms.openai_like import OpenAILike

from augmentation.components.llms.openai_like.configuration import (
    OpenAILikeLLMConfiguration,
)
from core import SingletonFactory


class OpenaAILikeLLMFactory(SingletonFactory):
    """
    Factory for creating and managing OpenAI-like LLM instances.

    This singleton factory creates and caches OpenAILike instances
    based on the provided configuration. It ensures that only one
    instance is created for each unique configuration.

    Attributes:
        _configuration_class: The configuration class used to create instances.
    """

    _configuration_class: Type = OpenAILikeLLMConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: OpenAILikeLLMConfiguration
    ) -> OpenAILike:
        """
        Create a new OpenAILike LLM instance based on the provided configuration.

        This method extracts the necessary parameters from the configuration
        object and initializes an OpenAILike instance with the appropriate
        settings for API access and model behavior.

        Args:
            configuration: Configuration object containing API credentials
                           and model parameters

        Returns:
            A configured OpenAILike instance ready for use
        """
        return OpenAILike(
            api_base=configuration.secrets.api_base.get_secret_value(),
            api_key=configuration.secrets.api_key.get_secret_value(),
            model=configuration.name,
            max_tokens=configuration.max_tokens,
            max_retries=configuration.max_retries,
            context_window=configuration.context_window,
            logprobs=None,
            api_version="",
        )
