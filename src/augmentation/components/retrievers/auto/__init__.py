from augmentation.bootstrap.configuration.components.retriever_configuration import (
    RetrieverConfigurationRegistry,
    RetrieverName,
)
from augmentation.components.retrievers.auto.configuration import (
    AutoRetrieverConfiguration,
)
from augmentation.components.retrievers.auto.retriever import (
    AutoRetrieverFactory,
)
from augmentation.components.retrievers.registry import RetrieverRegistry


def register() -> None:
    RetrieverConfigurationRegistry.register(
        RetrieverName.AUTO, AutoRetrieverConfiguration
    )
    RetrieverRegistry.register(RetrieverName.AUTO, AutoRetrieverFactory)
