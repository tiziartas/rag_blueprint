import logging
from typing import List, Type

from llama_index.core import StorageContext, VectorStoreIndex
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.schema import MetadataMode, TextNode
from llama_index.core.vector_stores.types import VectorStore

from core import Factory
from core.logger import LoggerConfiguration
from embedding.bootstrap.configuration.configuration import (
    EmbeddingConfiguration,
)
from embedding.embedders.base_embedder import BaseEmbedder
from embedding.embedding_models.registry import EmbeddingModelRegistry
from embedding.vector_stores.registry import VectorStoreRegistry


class BasicEmbedder(BaseEmbedder):
    """Implementation of text node embedding operations.

    Handles batch embedding generation and vector store persistence
    for text nodes.
    """

    def __init__(
        self,
        configuration: EmbeddingConfiguration,
        embedding_model: BaseEmbedding,
        vector_store: VectorStore,
        logger: logging.Logger = LoggerConfiguration.get_logger(__name__),
    ):
        """Initialize BasicEmbedder with model and storage.

        Args:
            configuration: Configuration for embedding process
            embedding_model: Model to generate embeddings
            vector_store: Storage for embedding vectors
            logger: Logger instance for tracking operations
        """
        super().__init__(configuration, embedding_model, vector_store)
        self.logger = logger
        self.batch_size = configuration.embedding.embedding_model.batch_size
        self.current_nodes_batch = []

    def embed(self, nodes: List[TextNode]) -> None:
        """Generate embeddings for text nodes in batches.

        Adds nodes to the current batch and processes complete batches
        when the batch size threshold is reached. Nodes are embedded
        and then saved to the vector store.

        Args:
            nodes: Collection of text nodes to embed

        Note:
            Modifies nodes in-place by setting embedding attribute
        """
        self.current_nodes_batch.extend(nodes)

        while len(self.current_nodes_batch) >= self.batch_size:
            batch = self.current_nodes_batch[: self.batch_size]
            self._embed_nodes_batch(batch)
            self._save_nodes_batch(batch)
            self.current_nodes_batch = self.current_nodes_batch[
                self.batch_size :
            ]

    def embed_flush(self) -> None:
        """Process any remaining nodes in the current batch.

        Ensures all nodes that haven't reached the batch size threshold
        are embedded and saved to the vector store before clearing the batch.
        Should be called after processing all documents to avoid losing
        the final incomplete batch.
        """
        if self.current_nodes_batch:
            self._embed_nodes_batch(self.current_nodes_batch)
            self._save_nodes_batch(self.current_nodes_batch)
            self.current_nodes_batch = []

    def _embed_nodes_batch(self, nodes: List[TextNode]) -> None:
        """Generate embeddings for a batch of text nodes.

        Extracts content from each node, generates embeddings using the embedding model,
        and assigns the resulting embeddings back to each node.

        Args:
            nodes: Batch of nodes to generate embeddings for
        """
        self.logger.info(f"Embedding batch of {len(nodes)} nodes.")
        nodes_contents = [
            node.get_content(metadata_mode=MetadataMode.EMBED) for node in nodes
        ]
        nodes_embeddings = self.embedding_model.get_text_embedding_batch(
            nodes_contents,
        )
        for node, node_embedding in zip(nodes, nodes_embeddings):
            node.embedding = node_embedding

    def _save_nodes_batch(self, nodes: List[TextNode]) -> None:
        """Save batch of text nodes to vector store.

        Creates a storage context with the configured vector store and
        stores the nodes with their embeddings using VectorStoreIndex.

        Args:
            nodes: Batch of nodes to save to the vector store
        """
        self.logger.info(f"Saving batch of {len(nodes)} nodes to vector store.")
        storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )
        VectorStoreIndex(
            nodes,
            storage_context=storage_context,
            embed_model=self.embedding_model,
        )


class BasicEmbedderFactory(Factory):
    _configuration_class: Type = EmbeddingConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: EmbeddingConfiguration
    ) -> BasicEmbedder:
        """Creates a configured BasicEmbedder instance.

        Initializes embedding model and vector store components based on
        the provided configuration settings.

        Args:
            configuration: Settings for embedding process configuration

        Returns:
            BasicEmbedder: Configured embedder instance ready for document processing
        """
        embedding_model_config = configuration.embedding.embedding_model
        embedding_model = EmbeddingModelRegistry.get(
            embedding_model_config.provider
        ).create(embedding_model_config)
        vector_store_config = configuration.embedding.vector_store
        vector_store = VectorStoreRegistry.get(vector_store_config.name).create(
            vector_store_config
        )
        return BasicEmbedder(
            configuration=configuration,
            embedding_model=embedding_model,
            vector_store=vector_store,
        )
