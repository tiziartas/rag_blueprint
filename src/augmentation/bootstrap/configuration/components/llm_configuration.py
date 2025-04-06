from enum import Enum
from typing import Type

from pydantic import Field

from core.base_configuration import BaseConfigurationWithSecrets
from core.base_factory import ConfigurationRegistry


# Enums
class LLMProviderName(str, Enum):
    OPENAI = "openai"
    OPENAI_LIKE = "openai-like"


# Configuration
class LLMConfiguration(BaseConfigurationWithSecrets):
    name: str = Field(..., description="The name of the language model.")
    max_tokens: int = Field(
        ..., description="The maximum number of tokens for the language model."
    )
    max_retries: int = Field(
        ..., description="The maximum number of retries for the language model."
    )


class LLMConfigurationRegistry(ConfigurationRegistry):
    _key_class: Type = LLMProviderName
