from typing import Type

from core import Registry
from embedding.bootstrap.configuration.configuration import (
    EmbeddingOrchestratorName,
)


class EmbeddingOrchestratorRegistry(Registry):
    _key_class: Type = EmbeddingOrchestratorName
