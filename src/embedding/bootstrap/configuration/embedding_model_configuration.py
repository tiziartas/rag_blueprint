from enum import Enum
from typing import Any, Type

from pydantic import Field, ValidationInfo, field_validator

from core import BaseConfigurationWithSecrets, ConfigurationRegistry
from embedding.bootstrap.configuration.splitting_configuration import (
    SplitterConfigurationRegistry,
)


# Enums
class EmbeddingModelProviderName(str, Enum):
    HUGGING_FACE = "hugging_face"
    OPENAI = "openai"
    VOYAGE = "voyage"


# Configuration
class EmbeddingModelConfiguration(BaseConfigurationWithSecrets):
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
        return super()._validate(
            value,
            info=info,
            registry=SplitterConfigurationRegistry,
        )


class EmbeddingModelConfigurationRegistry(ConfigurationRegistry):
    _key_class: Type = EmbeddingModelProviderName
