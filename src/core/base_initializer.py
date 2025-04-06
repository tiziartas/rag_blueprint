import importlib
import logging
import pkgutil
from abc import ABC, abstractmethod
from typing import List, Type

from core.base_configuration import BaseConfiguration, MetadataConfiguration
from core.configuration_retrievers import (
    BaseConfigurationRetriever,
    ConfiguratioRetriverRegistry,
)
from core.logger import LoggerConfiguration


class BaseInitializer(ABC):

    def __init__(self, configuration_class: Type[BaseConfiguration]):
        self._configuration_class = configuration_class

    @abstractmethod
    def get_configuration(self) -> BaseConfiguration:
        pass


class BasePackageLoader(ABC):

    def __init__(
        self, logger: logging.Logger = LoggerConfiguration.get_logger(__name__)
    ):
        self.logger = logger

    @abstractmethod
    def load_packages(self) -> None:
        """Load packages dynamically."""
        pass

    def _load_packages(self, parent_packages: List[str]) -> None:
        """Load packages from the specified parent packages."""

        for parent_package in parent_packages:
            self.logger.info(f"Loading {parent_package} packages...")
            package_path = parent_package.replace(".", "/")

            for _, name, is_package in pkgutil.iter_modules([package_path]):
                if is_package and name != "core":
                    try:
                        module_path = f"{parent_package}.{name}"
                        module = importlib.import_module(module_path)
                        module.register()
                        self.logger.info(f"Loaded package: {name}.")
                    except ImportError as e:
                        self.logger.error(
                            f"Failed to load datasource package {name}: {e}."
                        )
                    except Exception as e:
                        self.logger.error(
                            f"Failed to register package {name}: {e}."
                        )


class BasicInitializer(BaseInitializer):
    """Common initializer for embedding, augmentation and evaluation processes.

    Multiple components are used in the embedding, augmentation and evaluation processes.
    To avoid code duplication, this initializer is used to bind the components to the injector.
    It is intended to be subclassed by the specific initializers for each process.

    Attributes:
        configuration: Configuration object
        configuration_json: Configuration JSON string
    """

    def __init__(
        self,
        configuration_class: Type[BaseConfiguration],
        package_loader: BasePackageLoader,
    ):
        super().__init__(configuration_class)
        self.configuration_retriever: BaseConfigurationRetriever = None

        package_loader.load_packages()
        self._init_configuration_retriever()

    def get_configuration(self) -> BaseConfiguration:
        return self.configuration_retriever.get()

    def _init_configuration_retriever(self) -> None:
        metadata = MetadataConfiguration()
        configuration_retriever_class = ConfiguratioRetriverRegistry.get(
            on_prem=metadata.on_prem_config
        )
        self.configuration_retriever = configuration_retriever_class(
            configuration_class=self._configuration_class, metadata=metadata
        )
