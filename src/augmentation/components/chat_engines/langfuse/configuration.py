from pydantic import Field

from augmentation.bootstrap.configuration.components.chat_engine_configuration import (
    BaseChatEngineConfiguration,
    ChatEngineName,
)


class LangfuseChatEngineConfiguration(BaseChatEngineConfiguration):
    """
    Configuration class for the Langfuse chat engine.

    This class represents the configuration settings required for setting up and
    operating a chat engine with Langfuse integration. Langfuse provides observability
    and analytics capabilities for LLM applications.
    """

    name: ChatEngineName = Field(
        ChatEngineName.LANGFUSE,
        description="The name of the chat engine configuration integrated with langfuse.",
    )
