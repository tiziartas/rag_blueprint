from typing import Type

from augmentation.bootstrap.configuration.components.postprocessors_configuration import (
    PostProcessorName,
)
from core import Registry


class PostprocessorRegistry(Registry):
    """
    Registry for managing postprocessors in the RAG pipeline.

    This registry uses PostProcessorName as the key class to identify and retrieve
    different postprocessor implementations. Postprocessors are components that perform
    final transformations on data after the main processing is complete.

    Attributes:
        _key_class (Type): The class type used for registry keys, set to PostProcessorName.
    """

    _key_class: Type = PostProcessorName
