from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMConfigurationRegistry,
    LLMProviderName,
)
from augmentation.components.llms.openai_like.configuration import (
    OpenAILikeLLMConfiguration,
)
from augmentation.components.llms.openai_like.openai_like import (
    OpenaAILikeLLMFactory,
)
from augmentation.components.llms.registry import LLMRegistry


def register() -> None:
    LLMRegistry.register(LLMProviderName.OPENAI_LIKE, OpenaAILikeLLMFactory)
    LLMConfigurationRegistry.register(
        LLMProviderName.OPENAI_LIKE, OpenAILikeLLMConfiguration
    )
