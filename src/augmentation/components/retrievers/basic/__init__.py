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
    """Register Basic Retriever components with the system.

    This function registers the Basic Retriever configuration and factory
    with their respective registries. It connects the RetrieverName.BASIC
    identifier with both the configuration class and factory class, enabling
    the system to instantiate Basic Retrievers when requested.
    """
    RetrieverConfigurationRegistry.register(
        RetrieverName.BASIC, BasicRetrieverConfiguration
    )
    RetrieverRegistry.register(RetrieverName.BASIC, BasicRetrieverFactory)
