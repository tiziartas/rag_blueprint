from typing import Literal

from pydantic import ConfigDict, Field, SecretStr

from core.base_configuration import BaseSecrets
from embedding.bootstrap.configuration.vector_store_configuration import (
    VectorStoreConfiguration,
    VectorStoreName,
)


class PGVectorStoreConfiguration(VectorStoreConfiguration):
    """Configuration for PostgreSQL with pgvector extension as a vector store.

    This class provides all necessary configuration parameters to connect to
    and operate with a PostgreSQL database using the pgvector extension.
    """

    class Secrets(BaseSecrets):
        """Secret credentials required for authenticating with the PostgreSQL database.

        Handles environment variable loading with the RAG__VECTOR_STORE__ prefix.
        """

        model_config = ConfigDict(
            env_file_encoding="utf-8",
            env_prefix="RAG__VECTOR_STORE__",
            env_nested_delimiter="__",
            extra="ignore",
        )

        username: SecretStr = Field(
            ..., description="Username for PostgreSQL database authentication."
        )
        password: SecretStr = Field(
            ..., description="Password for PostgreSQL database authentication."
        )

    name: Literal[VectorStoreName.PGVECTOR] = Field(
        ..., description="The identifier of the vector store, must be PGVECTOR."
    )
    database_name: str = Field(
        ..., description="Name of the PostgreSQL database to connect to."
    )
    embed_dim: int = Field(
        384,
        description="Dimension of the vector embeddings stored in pgvector.",
    )
    secrets: Secrets = Field(
        None,
        description="Authentication credentials for the PostgreSQL database.",
    )
