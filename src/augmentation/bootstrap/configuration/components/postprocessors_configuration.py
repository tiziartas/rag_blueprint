from enum import Enum
from typing import List, Type

from pydantic import Field

from core.base_configuration import BaseConfiguration
from core.base_factory import ConfigurationRegistry


# Enums
class PostProcessorName(str, Enum):
    COLBERT_RERANK = "colbert_reranker"


# Configuration
class PostProcessorConfiguration(BaseConfiguration):
    name: PostProcessorName = Field(
        ..., description="The name of the postprocessor."
    )


class PostProcessorConfigurationRegistry(ConfigurationRegistry):
    _key_class: Type = PostProcessorName

    @classmethod
    def get_union_type(self) -> List[PostProcessorConfiguration]:
        """
        Returns the union type of all available datasources.
        """
        return List[super().get_union_type()]
