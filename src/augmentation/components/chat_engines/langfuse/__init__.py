from augmentation.bootstrap.configuration.components.chat_engine_configuration import (
    ChatEngineConfigurationRegistry,
    ChatEngineName,
)
from augmentation.components.chat_engines.langfuse.chat_engine import (
    LangfuseChatEngineFactory,
)
from augmentation.components.chat_engines.langfuse.configuration import (
    LangfuseChatEngineConfiguration,
)
from augmentation.components.chat_engines.registry import ChatEngineRegistry


def register() -> None:
    """
    Registers Langfuse chat engine components with the application registries.

    This function performs two registrations:
    1. Registers the LangfuseChatEngineConfiguration with the ChatEngineConfigurationRegistry
    2. Registers the LangfuseChatEngineFactory with the ChatEngineRegistry

    These registrations enable the Langfuse chat engine to be discovered and used
    by the RAG system, allowing integration with the Langfuse observability platform.
    """
    ChatEngineConfigurationRegistry.register(
        ChatEngineName.LANGFUSE, LangfuseChatEngineConfiguration
    )
    ChatEngineRegistry.register(
        ChatEngineName.LANGFUSE, LangfuseChatEngineFactory
    )
