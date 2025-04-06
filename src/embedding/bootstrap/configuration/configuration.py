from enum import Enum
from typing import Any

from pydantic import Field, ValidationInfo, field_validator

from core.base_configuration import BaseConfiguration
from embedding.bootstrap.configuration.embedding_model_configuration import (
    EmbeddingModelConfigurationRegistry,
)
from embedding.bootstrap.configuration.vector_store_configuration import (
    VectorStoreConfigurationRegistry,
)
from extraction.bootstrap.configuration.configuration import (
    ExtractionConfiguration,
)


class EmbeddingOrchestratorName(str, Enum):
    BASIC = "basic"


class EmbedderName(str, Enum):
    BASIC = "basic"


class _EmbeddingConfiguration(BaseConfiguration):
    vector_store: Any = Field(
        ...,
        description="Configuration of the vector store. Type is dynamically validated against configurations registered in `VetorStoreConfigurationRegistry`.",
    )
    embedding_model: Any = Field(
        ..., description="Configuration of the embedding model."
    )
    orchestrator_name: EmbeddingOrchestratorName = Field(
        EmbeddingOrchestratorName.BASIC,
        description="The name of the orchestrator to use for embedding.",
    )
    embedder_name: EmbedderName = Field(
        EmbedderName.BASIC,
        description="The name of the embedder to use for embedding.",
    )

    @field_validator("vector_store")
    @classmethod
    def _validate_vector_store(cls, value: Any, info: ValidationInfo) -> Any:
        return super()._validate(
            value,
            info=info,
            registry=VectorStoreConfigurationRegistry,
        )

    @field_validator("embedding_model")
    @classmethod
    def _validate_embedding_model(cls, value: Any, info: ValidationInfo) -> Any:
        return super()._validate(
            value,
            info=info,
            registry=EmbeddingModelConfigurationRegistry,
        )


class EmbeddingConfiguration(ExtractionConfiguration):
    embedding: _EmbeddingConfiguration = Field(
        ..., description="Configuration of the embedding process."
    )
