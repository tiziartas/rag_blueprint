from enum import Enum
from typing import Any, Type

from pydantic import Field, ValidationInfo, field_validator

from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMConfigurationRegistry,
)
from core.base_configuration import BaseConfiguration
from core.base_factory import ConfigurationRegistry


class SynthesizerName(str, Enum):
    """Enumeration of available synthesizer types."""

    TREE = "tree"


class SynthesizerConfiguration(BaseConfiguration):
    """Configuration class for response synthesizers.

    This class defines the parameters required to configure a synthesizer component
    that generates structured responses based on the provided configuration.
    """

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
        """Validate the LLM configuration.

        Ensures the provided language model configuration is valid according to the
        registered LLM configuration types.

        Args:
            value: The LLM configuration to validate.
            info: Validation context information.

        Returns:
            The validated LLM configuration object.
        """
        return super()._validate(
            value,
            info=info,
            registry=LLMConfigurationRegistry,
        )


class SynthesizerConfigurationRegistry(ConfigurationRegistry):
    """Registry for synthesizer configurations.

    Maintains a mapping between synthesizer names and their respective configuration classes,
    allowing for dynamic instantiation of synthesizer configurations based on their type.

    Attributes:
        _key_class: The enumeration class for synthesizer names.
    """

    _key_class: Type = SynthesizerName
