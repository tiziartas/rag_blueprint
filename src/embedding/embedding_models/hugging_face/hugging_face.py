from typing import Callable, Type

from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from transformers import AutoTokenizer

from core import SingletonFactory
from embedding.embedding_models.hugging_face.configuration import (
    HuggingFaceEmbeddingModelConfiguration,
)


class HuggingFaceEmbeddingModelFactory(SingletonFactory):
    """Factory for creating configured Qdrant clients."""

    _configuration_class: Type = HuggingFaceEmbeddingModelConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: HuggingFaceEmbeddingModelConfiguration
    ) -> HuggingFaceEmbedding:
        """Creates a Qdrant client based on provided configuration.

        Args:
            configuration: QDrant connection configuration.

        Returns:
            QdrantClient: Configured client instance.
        """
        return HuggingFaceEmbedding(
            model_name=configuration.name,
            embed_batch_size=configuration.batch_size,
        )


class HuggingFaceEmbeddingModelTokenizerFactory(SingletonFactory):
    _configuration_class: Type = HuggingFaceEmbeddingModelConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: HuggingFaceEmbeddingModelConfiguration
    ) -> Callable:
        return AutoTokenizer.from_pretrained(
            configuration.tokenizer_name
        ).tokenize
