from typing import Any, Literal

from pydantic import Field, ValidationInfo, field_validator

from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMConfigurationRegistry,
)
from augmentation.bootstrap.configuration.components.retriever_configuration import (
    RetrieverConfiguration,
    RetrieverName,
)


class AutoRetrieverConfiguration(RetrieverConfiguration):
    name: Literal[RetrieverName.AUTO] = Field(
        ..., description="The name of the retriever."
    )
    llm: Any = Field(
        ...,
        description="The LLM configuration used to extract metadata from the query.",
    )

    @field_validator("llm")
    @classmethod
    def _validate_llm(cls, value: Any, info: ValidationInfo) -> Any:
        return super()._validate(
            value,
            info=info,
            registry=LLMConfigurationRegistry,
        )
