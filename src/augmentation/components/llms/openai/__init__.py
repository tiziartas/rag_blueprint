from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMConfigurationRegistry,
    LLMProviderName,
)
from augmentation.components.llms.openai.configuration import (
    OpenAILLMConfiguration,
)
from augmentation.components.llms.openai.llm import OpenaAILLMFactory
from augmentation.components.llms.registry import LLMRegistry


def register() -> None:
    LLMRegistry.register(LLMProviderName.OPENAI, OpenaAILLMFactory)
    LLMConfigurationRegistry.register(
        LLMProviderName.OPENAI, OpenAILLMConfiguration
    )
