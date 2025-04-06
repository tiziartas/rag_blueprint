from typing import Type

from core import Registry
from extraction.bootstrap.configuration.datasources import DatasourceName


class DatasourceManagerRegistry(Registry):
    """Registry for datasource managers.

    This registry maps DatasourceName enums to their corresponding manager implementations.
    It provides a centralized way to register and retrieve datasource managers.

    Attributes:
        _key_class: Type of the key used in the registry (DatasourceName).
    """

    _key_class: Type = DatasourceName
