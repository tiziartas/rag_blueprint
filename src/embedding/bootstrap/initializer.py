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
    def __init__(
        self, logger: logging.Logger = LoggerConfiguration.get_logger(__name__)
    ):
        super().__init__(logger)

    def load_packages(self) -> None:
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
    """Common initializer for embedding, augmentation and evaluation processes.

    Multiple components are used in the embedding, augmentation and evaluation processes.
    To avoid code duplication, this initializer is used to bind the components to the injector.
    It is intended to be subclassed by the specific initializers for each process.

    Attributes:
        configuration: EmbeddingConfiguration object
        configuration_json: EmbeddingConfiguration JSON string
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
