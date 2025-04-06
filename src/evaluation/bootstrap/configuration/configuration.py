from typing import Any

from pydantic import Field, ValidationInfo, field_validator

from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMConfigurationRegistry,
)
from augmentation.bootstrap.configuration.configuration import (
    AugmentationConfiguration,
)
from core.base_configuration import BaseConfiguration
from embedding.bootstrap.configuration.embedding_model_configuration import (
    EmbeddingModelConfigurationRegistry,
)


class _EvaluationConfiguration(BaseConfiguration):
    judge_llm: Any = Field(
        ...,
        description="The judge language model configuration for the evaluation pipeline.",
    )
    judge_embedding_model: Any = Field(
        ...,
        description="The judge embedding model configuration for the evaluation pipeline.",
    )

    @field_validator("judge_llm")
    @classmethod
    def _validate_judge_llm(cls, value: Any, info: ValidationInfo) -> Any:
        return super()._validate(
            value,
            info=info,
            registry=LLMConfigurationRegistry,
        )

    @field_validator("judge_embedding_model")
    @classmethod
    def _validate_judge_embedding_model(
        cls, value: Any, info: ValidationInfo
    ) -> Any:
        return super()._validate(
            value,
            info=info,
            registry=EmbeddingModelConfigurationRegistry,
        )


class EvaluationConfiguration(AugmentationConfiguration):
    evaluation: _EvaluationConfiguration = Field(
        ..., description="Configuration of the augmentation process."
    )
