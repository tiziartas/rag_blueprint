from typing import Type

from core import Registry
from embedding.bootstrap.configuration.splitting_configuration import (
    SplitterName,
)


class SplitterRegistry(Registry):
    """
    Registry for document splitters that manages the registration and retrieval of different splitter implementations.

    This registry maps SplitterName enum values to their corresponding splitter implementations,
    allowing for a centralized way to access different text splitting strategies throughout the application.

    Attributes:
        _key_class: The class type used as keys in the registry, set to SplitterName enum.
    """

    _key_class: Type = SplitterName
