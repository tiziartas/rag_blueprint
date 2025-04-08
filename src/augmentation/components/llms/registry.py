from typing import Type

from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMProviderName,
)
from core import Registry


class LLMRegistry(Registry):
    """
    Registry for Large Language Model providers.

    This registry maps LLM provider names (defined in LLMProviderName enum)
    to their corresponding implementation classes. It allows for dynamic
    registration and retrieval of LLM provider implementations based on
    their enumerated types.

    Attributes:
        _key_class (Type): The class used as the key for the registry.
    """

    _key_class: Type = LLMProviderName


class LlamaindexLLMOutputExtractorRegistry(Registry):
    """
    Registry for Llamaindex LLM Output Extractors.

    This registry maps Llamaindex LLM Output Extractor names to their
    corresponding implementation classes. It allows for dynamic registration
    and retrieval of Llamaindex LLM Output Extractor implementations based on
    their enumerated types.

    Attributes:
        _key_class (Type): The class used as the key for the registry.
    """

    _key_class: Type = LLMProviderName
