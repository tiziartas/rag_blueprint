from enum import Enum
from typing import Any, List, Type

from pydantic import Field, ValidationInfo, field_validator

from augmentation.bootstrap.configuration.components.postprocessors_configuration import (
    PostProcessorConfigurationRegistry,
)
from augmentation.bootstrap.configuration.components.retriever_configuration import (
    RetrieverConfigurationRegistry,
)
from augmentation.bootstrap.configuration.components.synthesizer_configuration import (
    SynthesizerConfigurationRegistry,
)
from core.base_configuration import BaseConfiguration
from core.base_factory import ConfigurationRegistry


class QueryEngineName(str, Enum):
    """Enum defining available query engine types."""

    LANGFUSE = "langfuse"


class BaseQueryEngineConfiguration(BaseConfiguration):
    """Base configuration class for query engines.

    This class defines the standard configuration structure for all query engines,
    including retriever, synthesizer, and postprocessor components.
    """

    retriever: Any = Field(
        ...,
        description="The retriever configuration for the augmentation pipeline.",
    )
    synthesizer: Any = Field(
        ..., description="The synthesizer configuration for the query engine."
    )
    postprocessors: List[Any] = Field(
        ..., description="The list of postprocessors for the synthesizer."
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

    @field_validator("synthesizer")
    @classmethod
    def _validate_synthesizer(cls, value: Any, info: ValidationInfo) -> Any:
        """Validate synthesizer configuration against registered synthesizer types.

        Args:
            value: The synthesizer configuration to validate
            info: Validation context information

        Returns:
            Validated synthesizer configuration
        """
        return super()._validate(
            value,
            info=info,
            registry=SynthesizerConfigurationRegistry,
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


class QueryEngineConfigurationRegistry(ConfigurationRegistry):
    """Registry for query engine configurations.

    Maps query engine names to their corresponding configuration classes
    to facilitate configuration validation and factory creation.

    Attributes:
        _key_class: The enumeration class for query engine names.
    """

    _key_class: Type = QueryEngineName
