from pydantic import Field

from augmentation.bootstrap.configuration.components.query_engine_configuration import (
    BaseQueryEngineConfiguration,
    QueryEngineName,
)


class LangfuseQueryEngineConfiguration(BaseQueryEngineConfiguration):
    name: QueryEngineName = Field(
        QueryEngineName.LANGFUSE,
        description="The name of the query engine configuration integrated with langfuse.",
    )
