from typing import Type

from langfuse.api.resources.commons.types.trace_with_details import (
    TraceWithDetails,
)

from augmentation.components.llms.core.base_output_extractor import (
    BaseLlamaindexLLMOutputExtractor,
)
from augmentation.components.llms.openai.configuration import (
    OpenAILLMConfiguration,
)
from core.base_factory import Factory


class OpenAILlamaindexLLMOutputExtractor(BaseLlamaindexLLMOutputExtractor):
    """OpenAI Llamaindex LLM Output Extractor."""

    def get_text(self, trace: TraceWithDetails) -> str:
        """
        Extracts the text from the trace output.

        Args:
            trace (TraceWithDetails): The trace with details.

        Returns:
            str: The extracted text.
        """
        return trace.output["blocks"][0]["text"]

    def get_generated_by_model(self, trace: TraceWithDetails) -> str:
        """
        Extracts the model name from the trace output.

        Args:
            trace (TraceWithDetails): The trace with details.

        Returns:
            str: The name of the model.
        """
        return self.configuration.name


class OpenAILlamaindexLLMOutputExtractorFactory(Factory):
    """Factory class to create OpenAILlamaindexLLMOutputExtractor instances."""

    _configuration_class: Type = OpenAILLMConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: OpenAILLMConfiguration
    ) -> OpenAILlamaindexLLMOutputExtractor:
        """Creates an instance of OpenAILlamaindexLLMOutputExtractor.

        Args:
            configuration (OpenAILLMConfiguration): The configuration for the LLM.

        Returns:
            OpenAILlamaindexLLMOutputExtractor: An instance of the extractor.
        """
        return OpenAILlamaindexLLMOutputExtractor(configuration)
