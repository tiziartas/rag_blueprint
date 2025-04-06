from typing import Type

from augmentation.bootstrap.configuration.components.synthesizer_configuration import (
    SynthesizerName,
)
from core import Registry


class SynthesizerRegistry(Registry):
    """
    Registry for synthesizer components.

    This class maintains a registry of synthesizer implementations indexed by their
    SynthesizerName enum values. It extends the base Registry class and specifies
    SynthesizerName as the key type for registration and lookup operations.

    Synthesizer components can be registered with this registry and later retrieved
    by their corresponding enum value.

    Attributes:
        _key_class: The enumeration class for synthesizer names.
    """

    _key_class: Type = SynthesizerName
