from typing import Literal

from pydantic import Field

from embedding.bootstrap.configuration.vector_store_configuration import (
    VectorStoreConfiguration,
    VectorStoreName,
)


class QDrantVectorStoreConfiguration(VectorStoreConfiguration):
    """
    Configuration settings specific to QDrant vector store.

    Extends the base VectorStoreConfiguration with QDrant-specific properties
    and functionality.
    """

    name: Literal[VectorStoreName.QDRANT] = Field(
        ..., description="The name of the vector store."
    )

    @property
    def url(self) -> str:
        """
        Constructs the full URL for connecting to the QDrant service.

        Returns:
            str: The complete URL with protocol, host, and port.
        """
        return f"{self.protocol}://{self.host}:{self.port}"
