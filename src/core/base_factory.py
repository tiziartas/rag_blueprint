from abc import ABC, abstractmethod
from typing import Any, Dict, Type, Union


class Factory(ABC):
    """
    Abstract Factory base class for creating instances based on configurations.

    This class implements the Factory pattern and provides a standardized way
    to create instances of objects based on their configuration.

    Attributes:
        _configuration_class (Type): The expected type of configuration objects.
    """

    _configuration_class: Type = None

    @classmethod
    @abstractmethod
    def _create_instance(cls, configuration: Any) -> Any:
        """
        Abstract method that must be implemented by subclasses to create instances.

        Args:
            configuration (Any): The configuration object used to create the instance.

        Returns:
            Any: A new instance created based on the provided configuration.
        """
        pass

    @classmethod
    def create(cls, configuration: Any) -> Any:
        """
        Create an instance based on the given configuration.

        Args:
            configuration (Any): The configuration object used to create the instance. It has to be of the type specified by _configuration_class.

        Returns:
            Any: A new instance created based on the provided configuration.

        Raises:
            ValueError: If the configuration is not an instance of the expected type.
        """
        if not isinstance(configuration, cls._configuration_class):
            raise ValueError(
                f"Given configuration is {type(configuration)}, but must be of type type: {cls._configuration_class}"
            )
        return cls._create_instance(configuration)


class SingletonFactory(Factory):
    """
    This class extends the Factory pattern with Singleton functionality,
    ensuring that only one instance is created for each unique configuration
    during a single runtime.

    Attributes:
        _cache (dict): Dictionary storing instances by their configurations.
    """

    _cache: dict = {}

    def __init_subclass__(cls, **kwargs: Any):
        """
        Initialize a new subclass with an empty cache.

        This method is called when a subclass of SingletonFactory is created,
        ensuring each subclass has its own independent cache.

        Args:
            **kwargs: Additional keyword arguments.
        """
        super().__init_subclass__(**kwargs)
        cls._cache = {}

    @classmethod
    def create(cls, configuration: Any) -> Any:
        """
        Create or retrieve a singleton instance based on the given configuration.

        Args:
            configuration (Any): The configuration object used to create/retrieve the instance. It has to be of the type specified by _configuration_class.

        Returns:
            Any: A singleton instance associated with the provided configuration.

        Raises:
            ValueError: If the configuration is not an instance of the expected type.
        """
        if not isinstance(configuration, cls._configuration_class):
            raise ValueError(
                f"Given configuration is {type(configuration)}, but must be of type type: {cls._configuration_class}"
            )
        return cls._create_singleton(configuration)

    @classmethod
    def _create_singleton(cls, configuration: Any) -> Any:
        """
        Create a new instance or return an existing one from the cache.

        Args:
            configuration (Any): The configuration object used to create/retrieve the instance.

        Returns:
            Any: A singleton instance associated with the provided configuration.
        """
        if configuration in cls._cache:
            return cls._cache[configuration]
        instance = cls._create_instance(configuration)
        cls._cache[configuration] = instance
        return instance

    @classmethod
    def clear_cache(cls):
        """
        Clear the singleton instance cache.

        This method removes all cached instances, allowing them to be garbage collected.
        """
        cls._cache.clear()


class Registry:
    """
    A registry for storing and retrieving objects by key.

    This class implements a simple registry pattern that allows objects to be
    registered with a key and retrieved later using that key.
    It is designed to be subclassed, with each subclass defining its own
    expected key type.
    It is used for registering different plugins or components in a system.

    Attributes:
        _key_class (Type): The expected type for registry keys.
        _objects (Dict[Any, Any]): Dictionary storing registered objects by their keys.
    """

    _key_class: Type = None
    _objects: Dict[Any, Any] = {}

    def __init_subclass__(cls, **kwargs: Any):
        """
        Initialize a new subclass with an empty objects dictionary.

        This method is called when a subclass of Registry is created,
        ensuring each subclass has its own independent registry.

        Args:
            **kwargs: Additional keyword arguments.
        """
        super().__init_subclass__(**kwargs)
        cls._objects = {}

    @classmethod
    def register(cls, key: Any, Any: Any) -> None:
        """
        Register an object with the specified key.

        Args:
            key (Any): The key to associate with the object. Must be of type _key_class.
            Any (Any): The object to register.

        Raises:
            ValueError: If the key is not an instance of the expected type.
        """
        if not isinstance(key, cls._key_class):
            raise ValueError(f"Key must be of type: {cls._key_class}")
        cls._objects[key] = Any

    @classmethod
    def get(cls, key: Any) -> Any:
        """
        Retrieve an object by its key.

        Args:
            key (Any): The key associated with the object to retrieve.

        Returns:
            Any: The object associated with the key.

        Raises:
            ValueError: If no object is registered with the given key.
        """
        if key not in cls._objects:
            raise ValueError(f"Factory for '{key}' key is not registered.")
        return cls._objects[key]

    @classmethod
    def get_all(cls) -> Dict[Any, Any]:
        """
        Get all registered objects.

        Returns:
            Dict[Any, Any]: A dictionary containing all registered objects with their keys.
        """
        return cls._objects


class ConfigurationRegistry(Registry):
    """
    A specialized registry for configuration classes.

    This class extends the Registry to provide additional functionality
    specific to managing configuration classes, particularly the ability
    to create Union types from all registered configurations.
    The type is used by pydantic to validate the given configuration.
    """

    @classmethod
    def get_union_type(cls) -> Any:
        """
        Create a Union type of all registered configuration classes.

        This is useful for type hints where any of the registered
        configuration types can be accepted.

        Returns:
            Any: A Union type containing all registered configuration classes.
        """
        return Union[tuple(cls._objects.values())]
