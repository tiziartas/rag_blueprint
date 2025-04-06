from enum import Enum
from typing import Any, Type

from pydantic import Field, ValidationInfo, field_validator

from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMConfigurationRegistry,
)
from core.base_configuration import BaseConfiguration
from core.base_factory import ConfigurationRegistry


# Enums
class SynthesizerName(str, Enum):
    TREE = "tree"


# Configuraiton
class SynthesizerConfiguration(BaseConfiguration):
    name: SynthesizerName = Field(
        ..., description="The name of the synthesizer."
    )
    response_mode: str = Field(
        ..., description="The response mode of the synthesizer."
    )
    llm: Any = Field(
        ..., description="The language model configuration for the synthesizer."
    )
    streaming: bool = Field(
        True, description="Whether streaming is enabled for the synthesizer."
    )

    @field_validator("llm")
    @classmethod
    def _validate_llm(cls, value: Any, info: ValidationInfo) -> Any:
        return super()._validate(
            value,
            info=info,
            registry=LLMConfigurationRegistry,
        )


class SynthesizerConfigurationRegistry(ConfigurationRegistry):
    _key_class: Type = SynthesizerName
