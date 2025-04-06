from typing import Type

from llama_index.llms.openai import OpenAI

from augmentation.components.llms.openai.configuration import (
    OpenAILLMConfiguration,
)
from core import SingletonFactory


class OpenaAILLMFactory(SingletonFactory):
    """
    Factory class for creating OpenAI language model instances.

    This class implements the Singleton pattern to ensure only one instance
    of an OpenAI model with a specific configuration exists in the application.
    It uses OpenAILLMConfiguration to configure the model parameters.

    Attributes:
        _configuration_class: Type of the configuration class used for
            creating OpenAI model instances.
    """

    _configuration_class: Type = OpenAILLMConfiguration

    @classmethod
    def _create_instance(cls, configuration: OpenAILLMConfiguration) -> OpenAI:
        """
        Creates a new instance of the OpenAI language model.

        Args:
            configuration (OpenAILLMConfiguration): Configuration object containing
                settings for the OpenAI model, including API key, model name,
                maximum tokens, and retry settings.

        Returns:
            OpenAI: An instance of the OpenAI language model configured with the
                provided settings.
        """
        return OpenAI(
            api_key=configuration.secrets.api_key.get_secret_value(),
            model=configuration.name,
            max_tokens=configuration.max_tokens,
            max_retries=configuration.max_retries,
        )
