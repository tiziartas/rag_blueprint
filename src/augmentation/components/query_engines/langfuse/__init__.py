from augmentation.bootstrap.configuration.components.query_engine_configuration import (
    QueryEngineConfigurationRegistry,
    QueryEngineName,
)
from augmentation.components.query_engines.langfuse.configuration import (
    LangfuseQueryEngineConfiguration,
)
from augmentation.components.query_engines.langfuse.query_engine import (
    LangfuseQueryEngineFactory,
)
from augmentation.components.query_engines.registry import QueryEngineRegistry


def register() -> None:
    """
    Registers Langfuse query engine components with the application registries.

    This function performs two registrations:
    1. Registers the LangfuseQueryEngineConfiguration with the QueryEngineConfigurationRegistry
    2. Registers the LangfuseQueryEngineFactory with the QueryEngineRegistry

    These registrations enable the Langfuse query engine to be discovered and used
    by the RAG system, allowing integration with the Langfuse observability platform.
    """
    QueryEngineConfigurationRegistry.register(
        QueryEngineName.LANGFUSE, LangfuseQueryEngineConfiguration
    )
    QueryEngineRegistry.register(
        QueryEngineName.LANGFUSE, LangfuseQueryEngineFactory
    )
