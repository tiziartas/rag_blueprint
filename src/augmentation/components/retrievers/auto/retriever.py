from typing import Type

from llama_index.core import VectorStoreIndex
from llama_index.core.retrievers import VectorIndexAutoRetriever
from llama_index.core.vector_stores.types import MetadataInfo, VectorStoreInfo

from augmentation.bootstrap.configuration.configuration import (
    AugmentationConfiguration,
)
from augmentation.components.llms.registry import LLMRegistry
from core.base_factory import Factory
from embedding.embedding_models.registry import EmbeddingModelRegistry
from embedding.vector_stores.registry import VectorStoreRegistry


class AutoRetrieverFactory(Factory):
    _configuration_class: Type = AugmentationConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: AugmentationConfiguration
    ) -> VectorIndexAutoRetriever:
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
        llm = LLMRegistry.get(retriever_configuration.llm.provider).create(
            retriever_configuration.llm
        )

        return VectorIndexAutoRetriever(
            index=index,
            similarity_top_k=retriever_configuration.similarity_top_k,
            llm=llm,
            vector_store_info=VectorStoreInfo(
                content_info="Knowledge base of FELD M company used for retrieval process in RAG system.",
                metadata_info=[
                    MetadataInfo(
                        name="creation_date",
                        type="date",
                        description=(
                            "Date of creation of the chunk's document"
                        ),
                    ),
                    MetadataInfo(
                        name="last_update_date",
                        type="date",
                        description=(
                            "Date of the last update of the chunk's document."
                        ),
                    ),
                ],
            ),
        )
