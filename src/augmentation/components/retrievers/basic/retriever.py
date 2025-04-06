from typing import Type

from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexRetriever

from augmentation.bootstrap.configuration.configuration import (
    AugmentationConfiguration,
)
from core.base_factory import Factory
from embedding.embedding_models.registry import EmbeddingModelRegistry
from embedding.vector_stores.registry import VectorStoreRegistry


class BasicRetrieverFactory(Factory):
    _configuration_class: Type = AugmentationConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: AugmentationConfiguration
    ) -> VectorIndexRetriever:
        vector_store_configuration = configuration.embedding.vector_store
        vector_store = VectorStoreRegistry.get(
            vector_store_configuration.name
        ).create(vector_store_configuration)
        embedding_model_config = configuration.embedding.embedding_model
        embedding_model = EmbeddingModelRegistry.get(
            embedding_model_config.provider
        ).create(embedding_model_config)
        index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            embed_model=embedding_model,
        )

        retriever_configuration = (
            configuration.augmentation.query_engine.retriever
        )
        return VectorIndexRetriever(
            index=index,
            similarity_top_k=retriever_configuration.similarity_top_k,
        )
