from abc import ABC, abstractmethod
from typing import Any, Dict, Type, Union


class Factory(ABC):
    _configuration_class: Type = None

    @classmethod
    @abstractmethod
    def _create_instance(cls, configuration: Any) -> Any:
        pass

    @classmethod
    def create(cls, configuration: Any) -> Any:
        if not isinstance(configuration, cls._configuration_class):
            raise ValueError(
                f"Given configuration is {type(configuration)}, but must be of type type: {cls._configuration_class}"
            )
        return cls._create_instance(configuration)


class SingletonFactory(Factory):
    _cache: dict = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._cache = {}

    @classmethod
    def create(cls, configuration: Any) -> Any:
        if not isinstance(configuration, cls._configuration_class):
            raise ValueError(
                f"Given configuration is {type(configuration)}, but must be of type type: {cls._configuration_class}"
            )
        return cls._create_singleton(configuration)

    @classmethod
    def _create_singleton(cls, configuration: Any) -> Any:
        if configuration in cls._cache:
            return cls._cache[configuration]
        instance = cls._create_instance(configuration)
        cls._cache[configuration] = instance
        return instance

    @classmethod
    def clear_cache(cls):
        cls._cache.clear()


class Registry:
    _key_class: Type = None
    _objects: Dict[Any, Any] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls._objects = {}

    @classmethod
    def register(cls, key: Any, Any: Any) -> None:
        if not isinstance(key, cls._key_class):
            raise ValueError(f"Key must be of type: {cls._key_class}")
        cls._objects[key] = Any

    @classmethod
    def get(cls, key: Any) -> Any:
        if key not in cls._objects:
            raise ValueError(f"Factory for '{key}' key is not registered.")
        return cls._objects[key]

    @classmethod
    def get_all(cls) -> Dict[Any, Any]:
        return cls._objects


class ConfigurationRegistry(Registry):

    @classmethod
    def get_union_type(cls) -> Any:
        return Union[tuple(cls._objects.values())]
