from typing import Type

from langfuse.api.resources.commons.types.trace_with_details import (
    TraceWithDetails,
)

from augmentation.components.llms.core.base_output_extractor import (
    BaseLlamaindexLLMOutputExtractor,
)
from augmentation.components.llms.openai_like.configuration import (
    OpenAILikeLLMConfiguration,
)
from core.base_factory import Factory


class OpenAILikeLlamaindexLLMOutputExtractor(BaseLlamaindexLLMOutputExtractor):
    """OpenAI Llamaindex LLM Output Extractor."""

    def get_text(self, trace: TraceWithDetails) -> str:
        """
        Extracts the text from the trace output.

        Args:
            trace (TraceWithDetails): The trace with details.

        Returns:
            str: The extracted text.
        """
        return trace.output["text"]

    def get_generated_by_model(self, trace: TraceWithDetails) -> str:
        """
        Extracts the model name from the trace output.

        Args:
            trace (TraceWithDetails): The trace with details.

        Returns:
            str: The name of the model.
        """
        return trace.output["raw"]["model"]


class OpenAILikeLlamaindexLLMOutputExtractorFactory(Factory):
    """Factory class to create OpenAILikeLlamaindexLLMOutputExtractor instances."""

    _configuration_class: Type = OpenAILikeLLMConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: OpenAILikeLLMConfiguration
    ) -> OpenAILikeLlamaindexLLMOutputExtractor:
        """Creates an instance of OpenAILikeLlamaindexLLMOutputExtractor.

        Args:
            configuration (OpenAILikeLLMConfiguration): The configuration for the LLM.

        Returns:
            OpenAILikeLlamaindexLLMOutputExtractor: An instance of the extractor.
        """
        return OpenAILikeLlamaindexLLMOutputExtractor(configuration)
