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
    QueryEngineConfigurationRegistry.register(
        QueryEngineName.LANGFUSE, LangfuseQueryEngineConfiguration
    )
    QueryEngineRegistry.register(
        QueryEngineName.LANGFUSE, LangfuseQueryEngineFactory
    )
