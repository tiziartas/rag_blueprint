from typing import Type

from llama_index.llms.openai import OpenAI

from augmentation.components.llms.openai.configuration import (
    OpenAILLMConfiguration,
)
from core import SingletonFactory


class OpenaAILLMFactory(SingletonFactory):
    _configuration_class: Type = OpenAILLMConfiguration

    @classmethod
    def _create_instance(cls, configuration: OpenAILLMConfiguration) -> OpenAI:
        return OpenAI(
            api_key=configuration.secrets.api_key.get_secret_value(),
            model=configuration.name,
            max_tokens=configuration.max_tokens,
            max_retries=configuration.max_retries,
        )
