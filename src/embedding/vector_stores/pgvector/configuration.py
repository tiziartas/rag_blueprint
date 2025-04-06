from typing import Literal

from pydantic import ConfigDict, Field, SecretStr

from core.base_configuration import BaseSecrets
from embedding.bootstrap.configuration.vector_store_configuration import (
    VectorStoreConfiguration,
    VectorStoreName,
)


class PGVectorStoreConfiguration(VectorStoreConfiguration):
    class Secrets(BaseSecrets):
        model_config = ConfigDict(
            env_file_encoding="utf-8",
            env_prefix="RAG__VECTOR_STORE__",
            env_nested_delimiter="__",
            extra="ignore",
        )

        username: SecretStr = Field(
            ..., description="Username for the vector store."
        )
        password: SecretStr = Field(
            ..., description="Password for the vector store."
        )

    name: Literal[VectorStoreName.PGVECTOR] = Field(
        ..., description="The name of the vector store."
    )
    database_name: str = Field(..., description="The name of the database.")
    embed_dim: int = Field(384, description="The embedding dimension.")
    secrets: Secrets = Field(
        None, description="The secrets for the vector store."
    )
