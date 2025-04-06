from typing import Type

from augmentation.bootstrap.configuration.components.query_engine_configuration import (
    QueryEngineName,
)
from core import Registry


class QueryEngineRegistry(Registry):
    _key_class: Type = QueryEngineName
