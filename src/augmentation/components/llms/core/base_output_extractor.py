from abc import ABC, abstractmethod

from langfuse.api.resources.commons.types.trace_with_details import (
    TraceWithDetails,
)

from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMConfiguration,
)


class BaseLlamaindexLLMOutputExtractor(ABC):
    """Output field within `TraceWithDetails` is a dictionary, which structure
    depends on the LLM provider. This class provides an interface for extracting
    the text and model name from the output field of `TraceWithDetails` for
    different LLM providers. The actual extraction logic is implemented in
    subclasses for each specific LLM provider.
    """

    def __init__(self, configuration: LLMConfiguration):
        """Initializes the output extractor with the given configuration.

        Args:
            configuration (LLMConfiguration): The configuration for the LLM.
        """
        self.configuration = configuration

    @abstractmethod
    def get_text(cls, trace: TraceWithDetails) -> str:
        """Extracts the text from the trace.

        Args:
            trace (TraceWithDetails): The trace object containing the output.

        Returns:
            str: The extracted text.
        """
        pass

    @abstractmethod
    def get_generated_by_model(cls, trace: TraceWithDetails) -> str:
        """Extracts the model used to generate the output from the trace.

        Args:
            trace (TraceWithDetails): The trace object containing the output.

        Returns:
            str: The model name.
        """
        pass
