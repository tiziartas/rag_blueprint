from typing import Literal

from pydantic import Field

from augmentation.bootstrap.configuration.components.synthesizer_configuration import (
    SynthesizerConfiguration,
    SynthesizerName,
)


class TreeSynthesizerConfiguration(SynthesizerConfiguration):
    name: Literal[SynthesizerName.TREE] = Field(
        ..., description="The name of the synthesizer."
    )
    response_mode: str = Field(
        "tree_summarize", description="The response mode of the synthesizer."
    )
