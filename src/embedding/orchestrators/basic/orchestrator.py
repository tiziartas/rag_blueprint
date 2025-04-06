from typing import Type

from core import Factory
from embedding.bootstrap.configuration.configuration import (
    EmbeddingConfiguration,
)
from embedding.embedders.registry import EmbedderRegistry
from embedding.orchestrators.base_orchestrator import BaseEmbeddingOrchestrator
from embedding.splitters.registry import SplitterRegistry
from extraction.orchestrators.registry import DatasourceOrchestratorRegistry


class BasicEmbeddingOrchestrator(BaseEmbeddingOrchestrator):

    async def embed(self) -> None:
        async for doc in self.datasource_orchestrator.full_refresh_sync():
            nodes = self.splitter.split(doc)
            self.embedder.embed(nodes)
        self.embedder.embed_flush()


class BasicEmbeddingOrchestratorFactory(Factory):
    _configuration_class: Type = EmbeddingConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: EmbeddingConfiguration
    ) -> BasicEmbeddingOrchestrator:
        datasource_orchestrator = DatasourceOrchestratorRegistry.get(
            configuration.extraction.orchestrator_name
        ).create(configuration)

        embedding_model_configuration = configuration.embedding.embedding_model
        splitter_configuration = embedding_model_configuration.splitter
        if not splitter_configuration:
            raise ValueError(
                "Splitter configuration is required for embedding process."
            )
        splitter = SplitterRegistry.get(splitter_configuration.name).create(
            embedding_model_configuration
        )
        embedder = EmbedderRegistry.get(
            configuration.embedding.embedder_name
        ).create(configuration)
        return BasicEmbeddingOrchestrator(
            datasource_orchestrator=datasource_orchestrator,
            splitter=splitter,
            embedder=embedder,
        )
