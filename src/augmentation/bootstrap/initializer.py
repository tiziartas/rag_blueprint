import logging
from typing import Type

from augmentation.bootstrap.configuration.configuration import (
    AugmentationConfiguration,
)
from core.base_configuration import BaseConfiguration
from core.base_initializer import BasePackageLoader
from core.logger import LoggerConfiguration
from embedding.bootstrap.initializer import (
    EmbeddingInitializer,
    EmbeddingPackageLoader,
)


class AugmentationPackageLoader(EmbeddingPackageLoader):
    """Package loader for augmentation components.

    Extends the EmbeddingPackageLoader to load additional packages required
    for the augmentation process, including LLMs, synthesizers, retrievers,
    postprocessors, and query engines.
    """

    def __init__(
        self, logger: logging.Logger = LoggerConfiguration.get_logger(__name__)
    ):
        """Initialize the AugmentationPackageLoader.

        Args:
            logger: Logger instance for logging information. Defaults to a logger
                   configured with the current module name.
        """
        super().__init__(logger)

    def load_packages(self) -> None:
        """Load all required packages for augmentation.

        Calls the parent class's load_packages method first to load embedding packages,
        then loads additional packages specific to augmentation.
        """
        super().load_packages()
        self._load_packages(
            [
                "src.augmentation.components.llms",
                "src.augmentation.components.synthesizers",
                "src.augmentation.components.retrievers",
                "src.augmentation.components.postprocessors",
                "src.augmentation.components.query_engines",
            ]
        )


class AugmentationInitializer(EmbeddingInitializer):
    """Initializer for the augmentation process.

    Extends the EmbeddingInitializer to set up the environment for augmentation tasks.
    This initializer is responsible for loading the required configuration and
    registering all necessary components with the dependency injection container.

    Multiple components are used in the embedding, augmentation and evaluation processes.
    To avoid code duplication, this initializer is used to bind the components to the injector.
    It is intended to be subclassed by the specific initializers for each process.
    """

    def __init__(
        self,
        configuration_class: Type[
            BaseConfiguration
        ] = AugmentationConfiguration,
        package_loader: BasePackageLoader = AugmentationPackageLoader(),
    ):
        """Initialize the AugmentationInitializer.

        Args:
            configuration_class: The configuration class to use for loading settings.
                                Defaults to AugmentationConfiguration.
            package_loader: Package loader instance responsible for loading required packages.
                           Defaults to a new AugmentationPackageLoader instance.
        """
        super().__init__(
            configuration_class=configuration_class,
            package_loader=package_loader,
        )
