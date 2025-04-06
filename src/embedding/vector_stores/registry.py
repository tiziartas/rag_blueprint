from typing import Type

from core.base_factory import Registry
from embedding.bootstrap.configuration.vector_store_configuration import (
    VectorStoreName,
)


class VectorStoreRegistry(Registry):
    _key_class: Type = VectorStoreName


class VectorStoreValidatorRegistry(Registry):
    _key_class: Type = VectorStoreName
