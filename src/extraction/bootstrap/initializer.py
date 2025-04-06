import logging
from typing import Type

from core import BasicInitializer
from core.base_configuration import BaseConfiguration
from core.base_initializer import BasePackageLoader
from core.logger import LoggerConfiguration
from extraction.bootstrap.configuration.configuration import (
    ExtractionConfiguration,
)


class ExtractionPackageLoader(BasePackageLoader):
    def __init__(
        self, logger: logging.Logger = LoggerConfiguration.get_logger(__name__)
    ):
        super().__init__(logger)

    def load_packages(self) -> None:
        super().load_packages()
        self._load_packages(
            ["src.extraction.datasources", "src.extraction.orchestrators"]
        )


class ExtractionInitializer(BasicInitializer):
    def __init__(
        self,
        configuration_class: Type[BaseConfiguration] = ExtractionConfiguration,
        package_loader: BasePackageLoader = ExtractionPackageLoader(),
    ):
        super().__init__(
            configuration_class=configuration_class,
            package_loader=package_loader,
        )
