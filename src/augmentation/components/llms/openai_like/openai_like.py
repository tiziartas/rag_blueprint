from typing import Type

from llama_index.llms.openai_like import OpenAILike

from augmentation.components.llms.openai_like.configuration import (
    OpenAILikeLLMConfiguration,
)
from core import SingletonFactory


class OpenaAILikeLLMFactory(SingletonFactory):
    _configuration_class: Type = OpenAILikeLLMConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: OpenAILikeLLMConfiguration
    ) -> OpenAILike:
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
