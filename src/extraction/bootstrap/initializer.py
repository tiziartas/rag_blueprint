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
    """
    Loader for extraction-related packages.

    Handles loading of extraction datasources and orchestrators packages.
    """

    def __init__(
        self, logger: logging.Logger = LoggerConfiguration.get_logger(__name__)
    ):
        """
        Initialize the extraction package loader.

        Args:
            logger: Logger instance for logging information
        """
        super().__init__(logger)

    def load_packages(self) -> None:
        """
        Load all required extraction packages.

        Loads datasources and orchestrators packages needed for extraction operations.
        """
        super().load_packages()
        self._load_packages(
            ["src.extraction.datasources", "src.extraction.orchestrators"]
        )


class ExtractionInitializer(BasicInitializer):
    """
    Initializer for the extraction module.

    Handles the initialization of extraction components including configuration
    and required packages.
    """

    def __init__(
        self,
        configuration_class: Type[BaseConfiguration] = ExtractionConfiguration,
        package_loader: BasePackageLoader = ExtractionPackageLoader(),
    ):
        """
        Initialize the extraction module.

        Args:
            configuration_class: Configuration class to use for extraction
            package_loader: Loader for required extraction packages
        """
        super().__init__(
            configuration_class=configuration_class,
            package_loader=package_loader,
        )
