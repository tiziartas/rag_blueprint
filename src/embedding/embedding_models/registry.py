from typing import Type

from core import Registry
from embedding.bootstrap.configuration.embedding_model_configuration import (
    EmbeddingModelProviderName,
)


class EmbeddingModelRegistry(Registry):
    _key_class: Type = EmbeddingModelProviderName


class EmbeddingModelTokenizerRegistry(Registry):
    _key_class: Type = EmbeddingModelProviderName
