from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMConfigurationRegistry,
    LLMProviderName,
)
from augmentation.components.llms.openai_like.configuration import (
    OpenAILikeLLMConfiguration,
)
from augmentation.components.llms.openai_like.llm import OpenaAILikeLLMFactory
from augmentation.components.llms.openai_like.output_extractor import (
    OpenAILikeLlamaindexLLMOutputExtractorFactory,
)
from augmentation.components.llms.registry import (
    LlamaindexLLMOutputExtractorRegistry,
    LLMRegistry,
)


def register() -> None:
    """
    Register OpenAI-like LLM components with the application's registry system.

    This function registers:
    1. The OpenAI-like LLM factory with the LLM registry
    2. The OpenAI-like LLM configuration with the LLM configuration registry

    Both registrations use the OPENAI_LIKE provider name as the key.
    """
    LLMRegistry.register(LLMProviderName.OPENAI_LIKE, OpenaAILikeLLMFactory)
    LLMConfigurationRegistry.register(
        LLMProviderName.OPENAI_LIKE, OpenAILikeLLMConfiguration
    )
    LlamaindexLLMOutputExtractorRegistry.register(
        LLMProviderName.OPENAI_LIKE,
        OpenAILikeLlamaindexLLMOutputExtractorFactory,
    )
