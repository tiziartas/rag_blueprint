from typing import Callable, Type

import tiktoken
from llama_index.embeddings.openai import OpenAIEmbedding

from core import SingletonFactory
from embedding.embedding_models.openai.configuration import (
    OpenAIEmbeddingModelConfiguration,
)


class OpenAIEmbeddingModelFactory(SingletonFactory):
    """Factory for creating configured Qdrant clients."""

    _configuration_class: Type = OpenAIEmbeddingModelConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: OpenAIEmbeddingModelConfiguration
    ) -> OpenAIEmbedding:
        """Creates a Qdrant client based on provided configuration.

        Args:
            configuration: QDrant connection configuration.

        Returns:
            QdrantClient: Configured client instance.
        """
        return OpenAIEmbedding(
            api_key=configuration.secrets.api_key.get_secret_value(),
            model_name=configuration.name,
            embed_batch_size=configuration.batch_size,
        )


class OpenAIEmbeddingModelTokenizerFactory(SingletonFactory):
    _configuration_class: Type = OpenAIEmbeddingModelConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: OpenAIEmbeddingModelConfiguration
    ) -> Callable:
        return tiktoken.encoding_for_model(configuration.tokenizer_name).encode
