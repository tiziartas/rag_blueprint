from abc import ABC
from enum import Enum
from typing import List, Optional

from pydantic import Field

from core import BaseConfigurationWithSecrets
from core.base_factory import ConfigurationRegistry


# Enums
class DatasourceName(str, Enum):
    """
    List of all available datasources.
    """

    CONFLUENCE = "confluence"
    NOTION = "notion"
    PDF = "pdf"


# Configuration
class DatasourceConfiguration(BaseConfigurationWithSecrets, ABC):
    name: DatasourceName = Field(
        ..., description="The name of the data source."
    )
    export_limit: Optional[int] = Field(
        None, description="The export limit for the data source."
    )


class DatasourceConfigurationRegistry(ConfigurationRegistry):
    _key_class = DatasourceName

    @classmethod
    def get_union_type(self) -> List[DatasourceConfiguration]:
        """
        Returns the union type of all available datasources.
        """
        return List[super().get_union_type()]
