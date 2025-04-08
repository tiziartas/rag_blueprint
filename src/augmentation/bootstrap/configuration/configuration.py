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
    """
    Internal configuration class for augmentation process settings.

    This class defines the structure for augmentation configuration including
    Langfuse monitoring, Chainlit UI, and Query Engine components.
    """

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
        """
        Validates the query engine configuration using the appropriate registry.

        Args:
            value: The query engine configuration value to validate
            info: Validation context information provided by Pydantic

        Returns:
            The validated query engine configuration
        """
        return super()._validate(
            value,
            info=info,
            registry=QueryEngineConfigurationRegistry,
        )


class AugmentationConfiguration(EmbeddingConfiguration):
    """
    Main configuration class for the augmentation module.

    Extends the base embedding configuration with additional augmentation-specific
    settings to provide a complete configuration for text augmentation processes.
    """

    augmentation: _AugmentationConfiguration = Field(
        ..., description="Configuration of the augmentation process."
    )
