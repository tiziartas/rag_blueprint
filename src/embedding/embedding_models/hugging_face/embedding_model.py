from typing import Callable, Type

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from transformers import AutoTokenizer

from core import SingletonFactory
from embedding.embedding_models.hugging_face.configuration import (
    HuggingFaceEmbeddingModelConfiguration,
)


class HuggingFaceEmbeddingModelFactory(SingletonFactory):
    """Factory for creating configured HuggingFace embedding models.

    This singleton factory creates and configures HuggingFaceEmbedding instances
    based on the provided configuration.

    Attributes:
        _configuration_class (Type): The configuration class used for creating instances.
    """

    _configuration_class: Type = HuggingFaceEmbeddingModelConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: HuggingFaceEmbeddingModelConfiguration
    ) -> HuggingFaceEmbedding:
        """Creates a HuggingFaceEmbedding instance based on provided configuration.

        Args:
            configuration: HuggingFace embedding model configuration.

        Returns:
            HuggingFaceEmbedding: Configured embedding model instance.
        """
        return HuggingFaceEmbedding(
            model_name=configuration.name,
            embed_batch_size=configuration.batch_size,
        )


class HuggingFaceEmbeddingModelTokenizerFactory(SingletonFactory):
    """Factory for creating HuggingFace tokenizer functions.

    This singleton factory creates and configures tokenizer functions for HuggingFace models
    based on the provided configuration.
    """

    _configuration_class: Type = HuggingFaceEmbeddingModelConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: HuggingFaceEmbeddingModelConfiguration
    ) -> Callable:
        """Creates a tokenizer function based on provided configuration.

        Args:
            configuration: HuggingFace embedding model configuration.

        Returns:
            Callable: A tokenize function from the configured tokenizer.
        """
        return AutoTokenizer.from_pretrained(
            configuration.tokenizer_name
        ).tokenize
