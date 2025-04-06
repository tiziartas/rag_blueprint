from typing import Callable, Type

from llama_index.embeddings.voyageai import VoyageEmbedding
from transformers import AutoTokenizer

from core import SingletonFactory
from embedding.embedding_models.voyage.configuration import (
    VoyageEmbeddingModelConfiguration,
)


class VoyageEmbeddingModelFactory(SingletonFactory):
    """Factory for creating configured Qdrant clients."""

    _configuration_class: Type = VoyageEmbeddingModelConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: VoyageEmbeddingModelConfiguration
    ) -> VoyageEmbedding:
        """Creates a Qdrant client based on provided configuration.

        Args:
            configuration: QDrant connection configuration.

        Returns:
            QdrantClient: Configured client instance.
        """
        return VoyageEmbedding(
            voyage_api_key=configuration.secrets.api_key.get_secret_value(),
            model_name=configuration.name,
            embed_batch_size=configuration.batch_size,
        )


class VoyageEmbeddingModelTokenizerFactory(SingletonFactory):
    _configuration_class: Type = VoyageEmbeddingModelConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: VoyageEmbeddingModelConfiguration
    ) -> Callable:
        return AutoTokenizer.from_pretrained(
            configuration.tokenizer_name
        ).tokenize
