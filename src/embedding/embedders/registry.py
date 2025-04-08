from typing import Type

from core import Registry
from embedding.bootstrap.configuration.configuration import EmbedderName


class EmbedderRegistry(Registry):
    """Registry for managing embedding models.

    This registry stores and provides access to embedding model implementations
    based on their corresponding EmbedderName enumeration values. It extends the
    base Registry class to provide type-safe access to embedders.

    Attributes:
        _key_class (Type): The class type used as keys in the registry, which is
            EmbedderName enum in this case.
    """

    _key_class: Type = EmbedderName
