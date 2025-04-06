from enum import Enum
from typing import Type

from core import BaseConfiguration, ConfigurationRegistry


# Enums
class SplitterName(str, Enum):
    BASIC_MARKDOWN = "basic-markdown"


class SplitterConfiguration(BaseConfiguration):
    pass


# Configuration
class SplitterConfigurationRegistry(ConfigurationRegistry):
    _key_class: Type = SplitterName
