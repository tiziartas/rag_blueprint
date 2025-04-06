from typing import Callable, Type

from llama_index.embeddings.voyageai import VoyageEmbedding
from transformers import AutoTokenizer

from core import SingletonFactory
from embedding.embedding_models.voyage.configuration import (
    VoyageEmbeddingModelConfiguration,
)


class VoyageEmbeddingModelFactory(SingletonFactory):
    """Factory for creating configured Voyage embedding models.

    This factory ensures only one instance of a Voyage embedding model
    is created for each configuration.

    Attributes:
        _configuration_class (Type): The configuration class for the Voyage embedding model.
    """

    _configuration_class: Type = VoyageEmbeddingModelConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: VoyageEmbeddingModelConfiguration
    ) -> VoyageEmbedding:
        """Creates a Voyage embedding model based on provided configuration.

        Args:
            configuration: Voyage embedding model configuration with API key and settings.

        Returns:
            VoyageEmbedding: Configured Voyage embedding model instance.
        """
        return VoyageEmbedding(
            voyage_api_key=configuration.secrets.api_key.get_secret_value(),
            model_name=configuration.name,
            embed_batch_size=configuration.batch_size,
        )


class VoyageEmbeddingModelTokenizerFactory(SingletonFactory):
    """Factory for creating tokenizers for Voyage embedding models.

    Provides a singleton tokenizer function based on the configuration.
    """

    _configuration_class: Type = VoyageEmbeddingModelConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: VoyageEmbeddingModelConfiguration
    ) -> Callable:
        """Creates a tokenizer function based on provided configuration.

        Args:
            configuration: Voyage embedding model configuration containing tokenizer name.

        Returns:
            Callable: A tokenizer function that can be used to tokenize input text.
        """
        return AutoTokenizer.from_pretrained(
            configuration.tokenizer_name
        ).tokenize
