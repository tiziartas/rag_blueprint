from pydantic import Field

from augmentation.bootstrap.configuration.components.query_engine_configuration import (
    BaseQueryEngineConfiguration,
    QueryEngineName,
)


class LangfuseQueryEngineConfiguration(BaseQueryEngineConfiguration):
    """
    Configuration class for the Langfuse query engine.

    This class represents the configuration settings required for setting up and
    operating a query engine with Langfuse integration. Langfuse provides observability
    and analytics capabilities for LLM applications.
    """

    name: QueryEngineName = Field(
        QueryEngineName.LANGFUSE,
        description="The name of the query engine configuration integrated with langfuse.",
    )
