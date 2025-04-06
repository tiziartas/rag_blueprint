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
    """
    Register the Auto Retriever components with the application registries.

    This function registers:
    1. The AutoRetrieverConfiguration with RetrieverConfigurationRegistry
    2. The AutoRetrieverFactory with RetrieverRegistry

    These registrations enable the automatic retriever to be instantiated
    through the standard retriever configuration and factory mechanisms.
    """
    RetrieverConfigurationRegistry.register(
        RetrieverName.AUTO, AutoRetrieverConfiguration
    )
    RetrieverRegistry.register(RetrieverName.AUTO, AutoRetrieverFactory)
