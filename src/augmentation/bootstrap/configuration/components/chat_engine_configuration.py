from enum import Enum
from typing import Any, List, Type

from pydantic import Field, ValidationInfo, field_validator

from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMConfigurationRegistry,
)
from augmentation.bootstrap.configuration.components.postprocessors_configuration import (
    PostProcessorConfigurationRegistry,
)
from augmentation.bootstrap.configuration.components.retriever_configuration import (
    RetrieverConfigurationRegistry,
)
from core.base_configuration import BaseConfiguration
from core.base_factory import ConfigurationRegistry


class ChatEngineName(str, Enum):
    """Enum defining available chat engine types."""

    LANGFUSE = "langfuse"


class BaseChatEngineConfiguration(BaseConfiguration):
    """Base configuration class for chat engines.

    This class defines the standard configuration structure for all chat engines,
    including retriever, llm, and postprocessor components.
    """

    retriever: Any = Field(
        ...,
        description="The retriever configuration for the augmentation pipeline.",
    )
    llm: Any = Field(
        ..., description="The llm configuration for the chat engine."
    )
    postprocessors: List[Any] = Field(
        ..., description="The list of postprocessors for the chat engine."
    )

    @field_validator("retriever")
    @classmethod
    def _validate_retriever(cls, value: Any, info: ValidationInfo) -> Any:
        """Validate retriever configuration against registered retriever types.

        Args:
            value: The retriever configuration to validate
            info: Validation context information

        Returns:
            Validated retriever configuration
        """
        return super()._validate(
            value,
            info=info,
            registry=RetrieverConfigurationRegistry,
        )

    @field_validator("llm")
    @classmethod
    def _validate_llm(cls, value: Any, info: ValidationInfo) -> Any:
        """Validate llm configuration against registered llm types.

        Args:
            value: The llm configuration to validate
            info: Validation context information

        Returns:
            Validated llm configuration
        """
        return super()._validate(
            value,
            info=info,
            registry=LLMConfigurationRegistry,
        )

    @field_validator("postprocessors")
    @classmethod
    def _validate_postprocessors(
        cls, value: Any, info: ValidationInfo
    ) -> List[Any]:
        """Validate postprocessors configuration against registered postprocessor types.

        Args:
            value: The postprocessor configurations to validate
            info: Validation context information

        Returns:
            List of validated postprocessor configurations
        """
        return super()._validate(
            value,
            info=info,
            registry=PostProcessorConfigurationRegistry,
        )


class ChatEngineConfigurationRegistry(ConfigurationRegistry):
    """Registry for chat engine configurations.

    Maps chat engine names to their corresponding configuration classes
    to facilitate configuration validation and factory creation.

    Attributes:
        _key_class: The enumeration class for chat engine names.
    """

    _key_class: Type = ChatEngineName
