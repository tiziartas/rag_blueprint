from typing import Type

from augmentation.bootstrap.configuration.components.retriever_configuration import (
    RetrieverName,
)
from core.base_factory import Registry


class RetrieverRegistry(Registry):
    _key_class: Type = RetrieverName
