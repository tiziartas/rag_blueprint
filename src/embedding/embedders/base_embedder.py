from abc import ABC, abstractmethod
from typing import List

from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores.types import VectorStore

from embedding.bootstrap.configuration.configuration import (
    EmbeddingConfiguration,
)


class BaseEmbedder(ABC):
    """Abstract base class for text node embedding operations.

    This class provides core functionality for embedding text nodes,
    with derived classes implementing specific embedding strategies.
    """

    def __init__(
        self,
        configuration: EmbeddingConfiguration,
        embedding_model: BaseEmbedding,
        vector_store: VectorStore,
    ):
        """Initialize embedder with configuration, model and storage.

        Args:
            configuration: Configuration parameters for the embedding process
            embedding_model: Model to generate text embeddings
            vector_store: Storage system for persisting embedding vectors
        """
        super().__init__()
        self.configuration = configuration
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    @abstractmethod
    def embed(self, nodes: List[TextNode]) -> None:
        """Generate embeddings for text nodes using batch processing.

        This method should implement a strategy for processing the provided nodes,
        potentially splitting them into batches for efficient embedding generation.

        Args:
            nodes: Collection of text nodes to embed

        Note:
            Implementation should modify nodes in-place by adding embeddings
        """
        pass

    @abstractmethod
    def embed_flush(self) -> None:
        """Process and generate embeddings for any remaining nodes.

        This method should handle any nodes that remain in the buffer, ensuring all nodes receive embeddings.

        Note:
            Should be called at the end of processing to ensure no nodes remain
            unembedded in the buffer
        """
        pass
