from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMConfigurationRegistry,
    LLMProviderName,
)
from augmentation.components.llms.openai.configuration import (
    OpenAILLMConfiguration,
)
from augmentation.components.llms.openai.llm import OpenaAILLMFactory
from augmentation.components.llms.openai.output_extractor import (
    OpenAILlamaindexLLMOutputExtractorFactory,
)
from augmentation.components.llms.registry import (
    LlamaindexLLMOutputExtractorRegistry,
    LLMRegistry,
)


def register() -> None:
    LLMRegistry.register(LLMProviderName.OPENAI, OpenaAILLMFactory)
    LLMConfigurationRegistry.register(
        LLMProviderName.OPENAI, OpenAILLMConfiguration
    )
    LlamaindexLLMOutputExtractorRegistry.register(
        LLMProviderName.OPENAI, OpenAILlamaindexLLMOutputExtractorFactory
    )
