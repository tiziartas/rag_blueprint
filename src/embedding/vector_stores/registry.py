from typing import Type

from core.base_factory import Registry
from embedding.bootstrap.configuration.vector_store_configuration import (
    VectorStoreName,
)


class VectorStoreRegistry(Registry):
    """
    Registry for vector store implementations.

    Maps VectorStoreName values to vector store implementation classes.
    Used for registering and retrieving different vector store backends
    that can be configured in the system.
    """

    _key_class: Type = VectorStoreName


class VectorStoreValidatorRegistry(Registry):
    """
    Registry for vector store validator implementations.

    Maps VectorStoreName values to validator classes responsible for
    validating vector store configurations before use.
    Validators ensure proper setup and connection parameters.
    """

    _key_class: Type = VectorStoreName
