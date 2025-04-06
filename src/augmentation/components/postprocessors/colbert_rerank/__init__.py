from augmentation.bootstrap.configuration.components.postprocessors_configuration import (
    PostProcessorConfigurationRegistry,
    PostProcessorName,
)
from augmentation.components.postprocessors.colbert_rerank.configuraiton import (
    ColbertRerankConfiguration,
)
from augmentation.components.postprocessors.colbert_rerank.postprocessor import (
    ColbertRerankFactory,
)
from augmentation.components.postprocessors.registry import (
    PostprocessorRegistry,
)


def register() -> None:
    """
    Registers the ColBERT reranker component with the postprocessor registry.

    This function registers both the ColbertRerankFactory and ColbertRerankConfiguration
    with their respective registries, making the ColBERT reranking capability
    available to the augmentation pipeline.
    """
    PostprocessorRegistry.register(
        PostProcessorName.COLBERT_RERANK, ColbertRerankFactory
    )
    PostProcessorConfigurationRegistry.register(
        PostProcessorName.COLBERT_RERANK, ColbertRerankConfiguration
    )
