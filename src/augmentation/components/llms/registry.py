from typing import Type

from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMProviderName,
)
from core import Registry


class LLMRegistry(Registry):
    _key_class: Type = LLMProviderName
