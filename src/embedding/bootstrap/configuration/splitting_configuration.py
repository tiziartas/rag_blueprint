from enum import Enum
from typing import Type

from core import BaseConfiguration, ConfigurationRegistry


# Enums
class SplitterName(str, Enum):
    """
    Enumeration of available text splitter types.

    Attributes:
        BASIC_MARKDOWN: A basic splitter for markdown documents.
    """

    BASIC_MARKDOWN = "basic-markdown"


class SplitterConfiguration(BaseConfiguration):
    """
    Base configuration class for text splitters.

    This class provides the foundation for defining specific configurations
    required by different text splitting algorithms.
    """

    pass


# Configuration
class SplitterConfigurationRegistry(ConfigurationRegistry):
    """
    Registry for managing different splitter configurations.

    This registry maps SplitterName enum values to their corresponding
    configuration classes, allowing for dynamic configuration selection
    based on the chosen splitter type.

    Attributes:
        _key_class: The type used as keys in the registry (SplitterName).
    """

    _key_class: Type = SplitterName
