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
    """
    Registers the Tree synthesizer component with the application's registry system.

    This function performs two registrations:
    1. Registers the TreeSynthesizerConfiguration with the configuration registry under the TREE name
    2. Registers the TreeSynthesizerFactory with the synthesizer registry under the TREE name

    These registrations enable the application to instantiate and configure Tree synthesizers
    when requested by name.
    """
    SynthesizerConfigurationRegistry.register(
        SynthesizerName.TREE, TreeSynthesizerConfiguration
    )
    SynthesizerRegistry.register(
        SynthesizerName.TREE,
        TreeSynthesizerFactory,
    )
