from abc import ABC
from enum import Enum
from typing import Literal, Union

from pydantic import Field

from core.base_configuration import BaseConfigurationWithSecrets
from core.base_factory import ConfigurationRegistry


# Enums
class VectorStoreName(str, Enum):
    """
    Enumeration of supported vector store providers.
    """

    QDRANT = "qdrant"
    CHROMA = "chroma"
    PGVECTOR = "pgvector"


# Configuration
class VectorStoreConfiguration(BaseConfigurationWithSecrets, ABC):
    """
    Abstract base configuration class for vector stores.

    Inherits from BaseConfigurationWithSecrets to handle secure configuration settings.
    All specific vector store configurations should inherit from this class.

    Attributes:
        port: The port number for connecting to the vector store server.
        collection_name: Name of the collection in the vector store.
        host: Hostname or IP address of the vector store server.
        protocol: Connection protocol (http or https).
    """

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
    """
    Registry for vector store configurations.

    Maps VectorStoreName enum values to their corresponding configuration classes.
    Used to retrieve the appropriate configuration based on the selected vector store.
    """

    _key_class = VectorStoreName
