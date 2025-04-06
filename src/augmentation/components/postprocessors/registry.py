from typing import Type

from augmentation.bootstrap.configuration.components.postprocessors_configuration import (
    PostProcessorName,
)
from core import Registry


class PostprocessorRegistry(Registry):
    _key_class: Type = PostProcessorName
