from typing import Any

from pydantic import Field, ValidationInfo, field_validator

from augmentation.bootstrap.configuration.chainlit_configuration import (
    ChainlitConfiguration,
)
from augmentation.bootstrap.configuration.components.query_engine_configuration import (
    QueryEngineConfigurationRegistry,
)
from augmentation.bootstrap.configuration.langfuse_configuration import (
    LangfuseConfiguration,
)
from core.base_configuration import BaseConfiguration
from embedding.bootstrap.configuration.configuration import (
    EmbeddingConfiguration,
)


class _AugmentationConfiguration(BaseConfiguration):
    langfuse: LangfuseConfiguration = Field(
        ..., description="Configuration of the Langfuse."
    )
    chainlit: ChainlitConfiguration = Field(
        ..., description="Configuration of the Chainlit."
    )
    query_engine: Any = Field(
        ..., description="Configuration of the Query Engine."
    )

    @field_validator("query_engine")
    @classmethod
    def _validate_query_engine(cls, value: Any, info: ValidationInfo) -> Any:
        return super()._validate(
            value,
            info=info,
            registry=QueryEngineConfigurationRegistry,
        )


class AugmentationConfiguration(EmbeddingConfiguration):
    augmentation: _AugmentationConfiguration = Field(
        ..., description="Configuration of the augmentation process."
    )
