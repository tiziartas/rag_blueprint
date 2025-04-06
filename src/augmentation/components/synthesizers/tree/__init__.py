from augmentation.bootstrap.configuration.components.synthesizer_configuration import (
    SynthesizerConfigurationRegistry,
    SynthesizerName,
)
from augmentation.components.synthesizers.registry import SynthesizerRegistry
from augmentation.components.synthesizers.tree.configuration import (
    TreeSynthesizerConfiguration,
)
from augmentation.components.synthesizers.tree.synthesizer import (
    TreeSynthesizerFactory,
)


def register() -> None:
    SynthesizerConfigurationRegistry.register(
        SynthesizerName.TREE, TreeSynthesizerConfiguration
    )
    SynthesizerRegistry.register(
        SynthesizerName.TREE,
        TreeSynthesizerFactory,
    )
