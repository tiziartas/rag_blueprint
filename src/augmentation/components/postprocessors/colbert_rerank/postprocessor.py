from typing import Type

from llama_index.postprocessor.colbert_rerank import ColbertRerank

from augmentation.components.postprocessors.colbert_rerank.configuraiton import (
    ColbertRerankConfiguration,
)
from core import Factory


class ColbertRerankFactory(Factory):
    """
    Factory for creating ColbertRerank instances.

    ColbertRerank is a postprocessor that reranks retrieved nodes using ColBERT,
    a neural information retrieval model that uses contextualized late interaction.
    This factory handles the creation of ColbertRerank objects based on the provided
    configuration.

    Attributes:
        _configuration_class (Type): The configuration class for the ColbertRerank.
    """

    _configuration_class: Type = ColbertRerankConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: ColbertRerankConfiguration
    ) -> ColbertRerank:
        """
        Creates a ColbertRerank instance based on the provided configuration.

        Args:
            configuration (ColbertRerankConfiguration): Configuration object containing
                parameters for the ColbertRerank instance.

        Returns:
            ColbertRerank: An initialized ColbertRerank postprocessor that can be used
                to rerank retrieved documents based on their relevance to the query.
        """
        return ColbertRerank(
            top_n=configuration.top_n,
            model=configuration.model.value,
            tokenizer=configuration.tokenizer.value,
            keep_retrieval_score=configuration.keep_retrieval_score,
        )
