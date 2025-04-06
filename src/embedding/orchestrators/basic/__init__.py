from embedding.bootstrap.configuration.configuration import (
    EmbeddingOrchestratorName,
)
from embedding.orchestrators.basic.orchestrator import (
    BasicEmbeddingOrchestratorFactory,
)
from embedding.orchestrators.registry import EmbeddingOrchestratorRegistry


def register() -> None:
    EmbeddingOrchestratorRegistry.register(
        EmbeddingOrchestratorName.BASIC,
        BasicEmbeddingOrchestratorFactory,
    )
