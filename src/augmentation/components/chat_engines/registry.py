from typing import Type

from augmentation.bootstrap.configuration.components.chat_engine_configuration import (
    ChatEngineName,
)
from core import Registry


class ChatEngineRegistry(Registry):
    """
    Registry for chat engine components.

    This registry provides a centralized mechanism for registering, retrieving, and managing
    chat engine implementations. Chat engines are indexed by their ChatEngineName enum value,
    allowing for dynamic selection and instantiation of different chat engine strategies.

    Attributes:
        _key_class (Type): The class type used for registry keys, set to ChatEngineName.
    """

    _key_class: Type = ChatEngineName
