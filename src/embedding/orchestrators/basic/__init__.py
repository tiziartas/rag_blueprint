from embedding.bootstrap.configuration.configuration import (
    EmbeddingOrchestratorName,
)
from embedding.orchestrators.basic.orchestrator import (
    BasicEmbeddingOrchestratorFactory,
)
from embedding.orchestrators.registry import EmbeddingOrchestratorRegistry


def register() -> None:
    """
    Registers the BasicEmbeddingOrchestratorFactory with the EmbeddingOrchestratorRegistry.

    This function adds the basic embedding orchestrator to the registry under the BASIC
    orchestrator name, making it available for use throughout the application. It should
    be called during application initialization to ensure the orchestrator is properly
    registered before it's needed.
    """
    EmbeddingOrchestratorRegistry.register(
        EmbeddingOrchestratorName.BASIC,
        BasicEmbeddingOrchestratorFactory,
    )
