import logging
from typing import Type

from core.base_configuration import BaseConfiguration
from core.base_initializer import BasePackageLoader
from core.logger import LoggerConfiguration
from embedding.bootstrap.configuration.configuration import (
    EmbeddingConfiguration,
)
from extraction.bootstrap.initializer import (
    ExtractionInitializer,
    ExtractionPackageLoader,
)


class EmbeddingPackageLoader(ExtractionPackageLoader):
    """Package loader for embedding components.

    Extends the ExtractionPackageLoader to include embedding-specific packages.
    Responsible for dynamically loading embedding-related modules into the application.

    Attributes:
        logger: Logger instance for logging package loading operations
    """

    def __init__(
        self, logger: logging.Logger = LoggerConfiguration.get_logger(__name__)
    ):
        super().__init__(logger)

    def load_packages(self) -> None:
        """Loads all required packages for embedding functionality.

        First loads extraction packages via the parent class, then loads
        embedding-specific packages including vector stores, embedding models,
        text splitters, embedders, and orchestrators.
        """
        super().load_packages()
        self._load_packages(
            [
                "src.embedding.vector_stores",
                "src.embedding.embedding_models",
                "src.embedding.splitters",
                "src.embedding.embedders",
                "src.embedding.orchestrators",
            ]
        )


class EmbeddingInitializer(ExtractionInitializer):
    """Initializer for embedding, augmentation and evaluation processes.

    Extends the ExtractionInitializer to provide specialized initialization for
    embedding-related functionality. Responsible for binding embedding components
    to the dependency injection container and preparing the environment for
    embedding, augmentation, and evaluation processes.

    Attributes:
        configuration: EmbeddingConfiguration object containing configuration parameters
        configuration_json: JSON string representation of the EmbeddingConfiguration
        package_loader: Loader responsible for importing required packages
    """

    def __init__(
        self,
        configuration_class: Type[BaseConfiguration] = EmbeddingConfiguration,
        package_loader: BasePackageLoader = EmbeddingPackageLoader(),
    ):
        super().__init__(
            configuration_class=configuration_class,
            package_loader=package_loader,
        )
