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
    """
    Configuration for the Auto Retriever component.

    The Auto Retriever automatically determines the most appropriate retrieval
    strategy based on the query content, using an LLM to analyze and extract
    relevant metadata from the query.
    """

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
        """
        Validates the LLM configuration using the LLMConfigurationRegistry.

        This validator ensures that the provided LLM configuration is valid
        according to the registered LLM configuration classes.

        Args:
            value: The LLM configuration value to validate.
            info: ValidationInfo object containing context about the validation.

        Returns:
            The validated LLM configuration object.
        """
        return super()._validate(
            value,
            info=info,
            registry=LLMConfigurationRegistry,
        )
