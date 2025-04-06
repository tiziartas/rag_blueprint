from typing import Type

from llama_index.postprocessor.colbert_rerank import ColbertRerank

from augmentation.components.postprocessors.colbert_rerank.configuraiton import (
    ColbertRerankConfiguration,
)
from core import Factory


class ColbertRerankFactory(Factory):
    _configuration_class: Type = ColbertRerankConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: ColbertRerankConfiguration
    ) -> ColbertRerank:
        return ColbertRerank(
            top_n=configuration.top_n,
            model=configuration.model.value,
            tokenizer=configuration.tokenizer.value,
            keep_retrieval_score=configuration.keep_retrieval_score,
        )
