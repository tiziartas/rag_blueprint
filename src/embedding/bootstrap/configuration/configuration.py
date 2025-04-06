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
    """
    Enumeration of supported embedding orchestrator types.

    Currently supports:
    - BASIC: The default basic orchestration strategy
    """

    BASIC = "basic"


class EmbedderName(str, Enum):
    """
    Enumeration of supported embedder implementations.

    Currently supports:
    - BASIC: The default basic embedder
    """

    BASIC = "basic"


class _EmbeddingConfiguration(BaseConfiguration):
    """
    Internal configuration class for embedding-specific settings.

    Handles vector store configuration, embedding model configuration,
    and selection of orchestration and embedding strategies.
    """

    vector_store: Any = Field(
        ...,
        description="Configuration of the vector store. Type is dynamically validated against configurations registered in `VectorStoreConfigurationRegistry`.",
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
        """
        Validates the vector store configuration against registered configurations.

        Args:
            value: The configuration value to validate
            info: Validation context information

        Returns:
            The validated configuration object
        """
        return super()._validate(
            value,
            info=info,
            registry=VectorStoreConfigurationRegistry,
        )

    @field_validator("embedding_model")
    @classmethod
    def _validate_embedding_model(cls, value: Any, info: ValidationInfo) -> Any:
        """
        Validates the embedding model configuration against registered configurations.

        Args:
            value: The configuration value to validate
            info: Validation context information

        Returns:
            The validated configuration object
        """
        return super()._validate(
            value,
            info=info,
            registry=EmbeddingModelConfigurationRegistry,
        )


class EmbeddingConfiguration(ExtractionConfiguration):
    """
    Complete configuration for the embedding process.

    Extends the extraction configuration with embedding-specific settings,
    creating a comprehensive configuration for the entire embedding pipeline.
    """

    embedding: _EmbeddingConfiguration = Field(
        ..., description="Configuration of the embedding process."
    )
