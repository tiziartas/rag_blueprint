from typing import Callable, Type

import tiktoken
from llama_index.embeddings.openai import OpenAIEmbedding

from core import SingletonFactory
from embedding.embedding_models.openai.configuration import (
    OpenAIEmbeddingModelConfiguration,
)


class OpenAIEmbeddingModelFactory(SingletonFactory):
    """Factory for creating configured OpenAI embedding models.

    This factory creates singleton instances of OpenAI embedding models
    based on the provided configuration.
    """

    _configuration_class: Type = OpenAIEmbeddingModelConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: OpenAIEmbeddingModelConfiguration
    ) -> OpenAIEmbedding:
        """Creates an OpenAI embedding model based on provided configuration.

        Args:
            configuration: OpenAI embedding model configuration.

        Returns:
            OpenAIEmbedding: Configured OpenAI embedding model instance.
        """
        return OpenAIEmbedding(
            api_key=configuration.secrets.api_key.get_secret_value(),
            model_name=configuration.name,
            embed_batch_size=configuration.batch_size,
        )


class OpenAIEmbeddingModelTokenizerFactory(SingletonFactory):
    """Factory for creating OpenAI tokenizer functions.

    This factory creates singleton instances of OpenAI tokenizer functions
    based on the provided configuration.
    """

    _configuration_class: Type = OpenAIEmbeddingModelConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: OpenAIEmbeddingModelConfiguration
    ) -> Callable:
        """Creates a tokenizer function for OpenAI models based on provided configuration.

        Args:
            configuration: OpenAI embedding model configuration.

        Returns:
            Callable: A tokenizer function that converts text to token IDs.
        """
        return tiktoken.encoding_for_model(configuration.tokenizer_name).encode
