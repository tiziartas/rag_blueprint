from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMConfigurationRegistry,
    LLMProviderName,
)
from augmentation.components.llms.lite_llm.configuration import (
    LiteLLMConfiguration,
)
from augmentation.components.llms.lite_llm.llm import LiteLLMFactory
from augmentation.components.llms.registry import LLMRegistry


def register() -> None:
    LLMConfigurationRegistry.register(
        LLMProviderName.LITE_LLM, LiteLLMConfiguration
    )
    LLMRegistry.register(LLMProviderName.LITE_LLM, LiteLLMFactory)
