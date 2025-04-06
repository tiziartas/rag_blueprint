from typing import Type

from augmentation.bootstrap.configuration.components.synthesizer_configuration import (
    SynthesizerName,
)
from core import Registry


class SynthesizerRegistry(Registry):
    _key_class: Type = SynthesizerName
