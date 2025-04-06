from typing import Literal

from pydantic import Field

from embedding.bootstrap.configuration.vector_store_configuration import (
    VectorStoreConfiguration,
    VectorStoreName,
)


class QDrantVectorStoreConfiguration(VectorStoreConfiguration):
    name: Literal[VectorStoreName.QDRANT] = Field(
        ..., description="The name of the vector store."
    )

    @property
    def url(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}"
