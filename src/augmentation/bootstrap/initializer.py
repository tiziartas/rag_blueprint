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
    def __init__(
        self, logger: logging.Logger = LoggerConfiguration.get_logger(__name__)
    ):
        super().__init__(logger)

    def load_packages(self) -> None:
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
        configuration_class: Type[
            BaseConfiguration
        ] = AugmentationConfiguration,
        package_loader: BasePackageLoader = AugmentationPackageLoader(),
    ):
        super().__init__(
            configuration_class=configuration_class,
            package_loader=package_loader,
        )
