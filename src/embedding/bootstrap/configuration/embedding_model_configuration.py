from enum import Enum
from typing import Any, Type

from pydantic import Field, ValidationInfo, field_validator

from core import BaseConfigurationWithSecrets, ConfigurationRegistry
from embedding.bootstrap.configuration.splitting_configuration import (
    SplitterConfigurationRegistry,
)


# Enums
class EmbeddingModelProviderName(str, Enum):
    """Enumeration of supported embedding model providers.

    This enum lists all the providers that can be used for embedding models.
    """

    HUGGING_FACE = "hugging_face"
    OPENAI = "openai"
    VOYAGE = "voyage"


# Configuration
class EmbeddingModelConfiguration(BaseConfigurationWithSecrets):
    """Configuration class for embedding models.

    This class defines the necessary parameters and settings for configuring
    an embedding model, including provider information, model name, and
    tokenization settings.
    """

    provider: EmbeddingModelProviderName = Field(
        ..., description="The provider of the embedding model."
    )
    name: str = Field(..., description="The name of the embedding model.")
    tokenizer_name: str = Field(
        ...,
        description="The name of the tokenizer used by the embedding model.",
    )
    batch_size: int = Field(64, description="The batch size for embedding.")

    splitter: Any = Field(
        None, description="The splitter configuration for the embedding model."
    )

    @field_validator("splitter")
    @classmethod
    def _validate_splitter(cls, value: Any, info: ValidationInfo) -> Any:
        """Validate the splitter configuration.

        This method ensures that the provided splitter configuration is valid
        according to the SplitterConfigurationRegistry.

        Args:
            value: The splitter configuration value to validate.
            info: Validation context information.

        Returns:
            The validated splitter configuration.
        """
        return super()._validate(
            value,
            info=info,
            registry=SplitterConfigurationRegistry,
        )


class EmbeddingModelConfigurationRegistry(ConfigurationRegistry):
    """Registry for embedding model configurations.

    This registry maps embedding model provider names to their
    respective configuration classes.
    """

    _key_class: Type = EmbeddingModelProviderName
