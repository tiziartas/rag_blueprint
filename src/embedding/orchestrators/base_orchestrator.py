from abc import ABC, abstractmethod

from embedding.embedders.base_embedder import BaseEmbedder
from embedding.splitters.base_splitter import BaseSplitter
from extraction.orchestrators.base_orchestator import BaseDatasourceOrchestrator


class BaseEmbeddingOrchestrator(ABC):
    """
    Abstract base class for embedding orchestration.

    This class defines the interface for embedding orchestrators that coordinate
    data extraction, splitting, and embedding processes.
    """

    def __init__(
        self,
        datasource_orchestrator: BaseDatasourceOrchestrator,
        splitter: BaseSplitter,
        embedder: BaseEmbedder,
    ) -> None:
        """
        Initialize a new embedding orchestrator.

        Args:
            datasource_orchestrator: Orchestrator for extracting data from sources
            splitter: Component responsible for splitting documents into nodes
            embedder: Component that generates embeddings for nodes
        """
        self.datasource_orchestrator = datasource_orchestrator
        self.splitter = splitter
        self.embedder = embedder

    @abstractmethod
    async def embed(self) -> None:
        """
        Execute the embedding process.

        This method must be implemented by concrete subclasses to define
        the specific embedding workflow.
        """
        pass


class BasicEmbeddingOrchestrator(BaseEmbeddingOrchestrator):
    """
    Basic implementation of embedding orchestration.

    This orchestrator implements a simple workflow that:
    1. Retrieves documents from the datasource
    2. Splits each document into nodes
    3. Embeds the nodes
    4. Flushes any remaining embeddings
    """

    async def embed(self) -> None:
        """
        Execute the basic embedding process.

        Retrieves documents asynchronously from the datasource orchestrator,
        splits each document into nodes, embeds the nodes, and finally
        flushes any remaining embeddings to ensure all data is processed.
        """
        async for doc in self.datasource_orchestrator.full_refresh_sync():
            nodes = self.splitter.split(doc)
            self.embedder.embed(nodes)
        self.embedder.embed_flush()
