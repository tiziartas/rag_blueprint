from augmentation.bootstrap.configuration.components.retriever_configuration import (
    RetrieverConfigurationRegistry,
    RetrieverName,
)
from augmentation.components.retrievers.basic.configuration import (
    BasicRetrieverConfiguration,
)
from augmentation.components.retrievers.basic.retriever import (
    BasicRetrieverFactory,
)
from augmentation.components.retrievers.registry import RetrieverRegistry


def register() -> None:
    RetrieverConfigurationRegistry.register(
        RetrieverName.BASIC, BasicRetrieverConfiguration
    )
    RetrieverRegistry.register(RetrieverName.BASIC, BasicRetrieverFactory)
