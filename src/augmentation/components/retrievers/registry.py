from typing import Type

from augmentation.bootstrap.configuration.components.retriever_configuration import (
    RetrieverName,
)
from core.base_factory import Registry


class RetrieverRegistry(Registry):
    """Registry for managing retriever components in the RAG system.

    This registry maps RetrieverName enum values to their corresponding retriever
    implementations, facilitating the creation and management of retriever instances
    based on configuration. It inherits from the base Registry class and specifies
    RetrieverName as the key type for registration and lookup operations.

    Attributes:
        _key_class (Type): The class type used for registry keys, set to RetrieverName enum.
    """

    _key_class: Type = RetrieverName
