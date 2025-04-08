from typing import Type

from augmentation.bootstrap.configuration.components.query_engine_configuration import (
    QueryEngineName,
)
from core import Registry


class QueryEngineRegistry(Registry):
    """
    Registry for query engine components.

    This registry provides a centralized mechanism for registering, retrieving, and managing
    query engine implementations. Query engines are indexed by their QueryEngineName enum value,
    allowing for dynamic selection and instantiation of different query engine strategies.

    Attributes:
        _key_class (Type): The class type used for registry keys, set to QueryEngineName.
    """

    _key_class: Type = QueryEngineName
