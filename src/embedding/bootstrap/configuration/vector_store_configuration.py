from abc import ABC
from enum import Enum
from typing import Literal, Union

from pydantic import Field

from core.base_configuration import BaseConfigurationWithSecrets
from core.base_factory import ConfigurationRegistry


# Enums
class VectorStoreName(str, Enum):
    QDRANT = "qdrant"
    CHROMA = "chroma"
    PGVECTOR = "pgvector"


# Configuration
class VectorStoreConfiguration(BaseConfigurationWithSecrets, ABC):
    port: int = Field(..., description="The port for the vector store.")
    collection_name: str = Field(
        ..., description="The collection name in the vector store."
    )
    host: str = Field(
        "127.0.0.1", description="Host of the vector store server"
    )
    protocol: Union[Literal["http"], Literal["https"]] = Field(
        "http", description="The protocol for the vector store."
    )


# Registry
class VectorStoreConfigurationRegistry(ConfigurationRegistry):
    _key_class = VectorStoreName
