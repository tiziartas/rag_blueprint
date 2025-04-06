from typing import Type

from core import Registry
from embedding.bootstrap.configuration.embedding_model_configuration import (
    EmbeddingModelProviderName,
)


class EmbeddingModelRegistry(Registry):
    """
    Registry for embedding models that maps provider names to their implementations.

    This registry uses EmbeddingModelProviderName as keys to store and retrieve
    embedding model implementations, allowing the system to support multiple
    embedding model providers while providing a uniform interface for registration
    and lookup.

    Attributes:
        _key_class: The class type used as keys in the registry, set to EmbeddingModelProviderName enum.
    """

    _key_class: Type = EmbeddingModelProviderName


class EmbeddingModelTokenizerRegistry(Registry):
    """
    Registry for embedding model tokenizers that maps provider names to their respective tokenizers.

    This registry uses EmbeddingModelProviderName as keys to store and retrieve
    tokenizer implementations that are compatible with specific embedding models.
    Tokenizers are used to preprocess text before embedding generation.

    Attributes:
        _key_class: The class type used as keys in the registry, set to EmbeddingModelProviderName enum.
    """

    _key_class: Type = EmbeddingModelProviderName
