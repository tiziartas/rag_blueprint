from typing import Literal

from pydantic import Field

from embedding.bootstrap.configuration.vector_store_configuration import (
    VectorStoreConfiguration,
    VectorStoreName,
)


class ChromaVectorStoreConfiguration(VectorStoreConfiguration):
    name: Literal[VectorStoreName.CHROMA] = Field(
        ..., description="The name of the vector store."
    )
