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
    LANGFUSE = "langfuse"


class BaseQueryEngineConfiguration(BaseConfiguration):
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
        return super()._validate(
            value,
            info=info,
            registry=RetrieverConfigurationRegistry,
        )

    @field_validator("synthesizer")
    @classmethod
    def _validate_synthesizer(cls, value: Any, info: ValidationInfo) -> Any:
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
        return super()._validate(
            value,
            info=info,
            registry=PostProcessorConfigurationRegistry,
        )


class QueryEngineConfigurationRegistry(ConfigurationRegistry):
    _key_class: Type = QueryEngineName
