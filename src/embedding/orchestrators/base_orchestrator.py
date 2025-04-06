from abc import ABC, abstractmethod

from embedding.embedders.base_embedder import BaseEmbedder
from embedding.splitters.base_splitter import BaseSplitter
from extraction.orchestrators.base_orchestator import BaseDatasourceOrchestrator


class BaseEmbeddingOrchestrator(ABC):

    def __init__(
        self,
        datasource_orchestrator: BaseDatasourceOrchestrator,
        splitter: BaseSplitter,
        embedder: BaseEmbedder,
    ) -> None:
        self.datasource_orchestrator = datasource_orchestrator
        self.splitter = splitter
        self.embedder = embedder

    @abstractmethod
    async def embed(self) -> None:
        pass


class BasicEmbeddingOrchestrator(BaseEmbeddingOrchestrator):

    async def embed(self) -> None:
        async for doc in self.datasource_orchestrator.full_refresh_sync():
            nodes = self.splitter.split(doc)
            self.embedder.embed(nodes)
        self.embedder.embed_flush()
