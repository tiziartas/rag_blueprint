from typing import Type

from llama_index.core import get_response_synthesizer
from llama_index.core.prompts.base import PromptTemplate
from llama_index.core.prompts.prompt_type import PromptType
from llama_index.postprocessor.colbert_rerank import ColbertRerank

from augmentation.bootstrap.configuration.configuration import (
    _AugmentationConfiguration,
)
from augmentation.components.llms.registry import LLMRegistry
from augmentation.langfuse.prompt_service import LangfusePromptServiceFactory
from core import Factory


class TreeSynthesizerFactory(Factory):
    """Factory class for creating tree-based response synthesizers.

    This factory creates response synthesizers that process and combine
    information from multiple sources into coherent, tree-structured responses.

    Attributes:
        _configuration_class: The configuration class for the tree synthesizer.
    """

    _configuration_class: Type = _AugmentationConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: _AugmentationConfiguration
    ) -> ColbertRerank:
        """Creates a response synthesizer instance based on the provided configuration.

        This method initializes a language model from the registry using the
        configuration's LLM settings, then creates a response synthesizer with
        the specified parameters and custom prompt template.

        Args:
            configuration: Configuration object containing response synthesizer settings
                          including LLM provider, response mode, and streaming options.

        Returns:
            A configured response synthesizer instance.
        """
        synthesizer_configuration = configuration.query_engine.synthesizer
        llm = LLMRegistry.get(synthesizer_configuration.llm.provider).create(
            synthesizer_configuration.llm
        )
        return get_response_synthesizer(
            llm=llm,
            response_mode=synthesizer_configuration.response_mode,
            streaming=synthesizer_configuration.streaming,
            summary_template=TreeSynthesizerFactory._get_prompt_template(
                configuration
            ),
        )

    @staticmethod
    def _get_prompt_template(
        configuration: _AugmentationConfiguration,
    ) -> PromptTemplate:
        """Retrieves the prompt template for the synthesizer.

        Args:
            configuration: Configuration object containing synthesizer settings.

        Returns:
            The prompt template to be used by the synthesizer.
        """
        langfuse_prompt_service = LangfusePromptServiceFactory.create(
            configuration=configuration.langfuse
        )
        prompt_template_str = langfuse_prompt_service.get_prompt_template(
            prompt_name=configuration.query_engine.synthesizer.prompt_name
        )
        return PromptTemplate(
            prompt_template_str, prompt_type=PromptType.SUMMARY
        )
