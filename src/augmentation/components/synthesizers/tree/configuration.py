from typing import Literal

from pydantic import Field

from augmentation.bootstrap.configuration.components.synthesizer_configuration import (
    SynthesizerConfiguration,
    SynthesizerName,
)


class TreeSynthesizerConfiguration(SynthesizerConfiguration):
    """
    Configuration class for the Tree Synthesizer component.

    The Tree Synthesizer hierarchically organizes and summarizes information,
    creating a tree-like structure of knowledge from input content. This enables
    better organization and condensation of information for RAG applications.

    This class extends the base SynthesizerConfiguration with tree-specific parameters.
    """

    name: Literal[SynthesizerName.TREE] = Field(
        ..., description="The name of the synthesizer."
    )
    response_mode: str = Field(
        "tree_summarize", description="The response mode of the synthesizer."
    )
