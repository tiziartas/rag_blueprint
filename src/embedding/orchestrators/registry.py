from typing import Type

from core import Registry
from embedding.bootstrap.configuration.configuration import (
    EmbeddingOrchestratorName,
)


class EmbeddingOrchestratorRegistry(Registry):
    """Registry for managing embedding orchestrators.

    This registry uses EmbeddingOrchestratorName as keys to store and retrieve
    orchestrator implementations. It extends the base Registry class to provide
    specialized functionality for embedding orchestration components.

    Attributes:
        _key_class: The class type used as keys in the registry, set to EmbeddingOrchestratorName enum.
    """

    _key_class: Type = EmbeddingOrchestratorName
