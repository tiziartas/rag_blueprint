from typing import Any

from pydantic import Field, ValidationInfo, field_validator

from augmentation.bootstrap.configuration.chainlit_configuration import (
    ChainlitConfiguration,
)
from augmentation.bootstrap.configuration.components.chat_engine_configuration import (
    ChatEngineConfigurationRegistry,
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
    Langfuse monitoring, Chainlit UI, and Chat Engine components.
    """

    langfuse: LangfuseConfiguration = Field(
        ..., description="Configuration of the Langfuse."
    )
    chainlit: ChainlitConfiguration = Field(
        ..., description="Configuration of the Chainlit."
    )
    chat_engine: Any = Field(
        ..., description="Configuration of the Chat Engine."
    )

    @field_validator("chat_engine")
    @classmethod
    def _validate_chat_engine(cls, value: Any, info: ValidationInfo) -> Any:
        """
        Validates the chat engine configuration using the appropriate registry.

        Args:
            value: The chat engine configuration value to validate
            info: Validation context information provided by Pydantic

        Returns:
            The validated chat engine configuration
        """
        return super()._validate(
            value,
            info=info,
            registry=ChatEngineConfigurationRegistry,
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
