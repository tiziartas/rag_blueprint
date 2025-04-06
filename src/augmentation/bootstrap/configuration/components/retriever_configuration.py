from enum import Enum
from typing import Type

from pydantic import Field

from core.base_configuration import BaseConfiguration
from core.base_factory import ConfigurationRegistry


# Enums
class RetrieverName(str, Enum):
    BASIC = "basic"
    AUTO = "auto"


# Configuration
class RetrieverConfiguration(BaseConfiguration):
    name: RetrieverName = Field(..., description="The name of the retriever.")
    similarity_top_k: int = Field(
        ..., description="The number of top similar items to retrieve."
    )


class RetrieverConfigurationRegistry(ConfigurationRegistry):
    _key_class: Type = RetrieverName
