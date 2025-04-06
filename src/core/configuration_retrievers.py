import logging
from abc import ABC, abstractmethod
from typing import Type

from core.base_configuration import BaseConfiguration, MetadataConfiguration
from core.logger import LoggerConfiguration


class BaseConfigurationRetriever(ABC):
    """Abstract base class for configuration retrieval.

    This class defines the common interface and functionality for retrieving
    application configurations from various sources. Concrete implementations
    should extend this class to provide specific retrieval mechanisms.

    Attributes:
        CONFIGURATIONS_DIR (str): Directory where configuration files are stored.
    """

    CONFIGURATIONS_DIR = "configurations"

    def __init__(
        self,
        configuration_class: Type[BaseConfiguration],
        metadata: MetadataConfiguration,
        logger: logging.Logger = LoggerConfiguration.get_logger(__name__),
    ):
        """Initialize the configuration retriever.

        Args:
            configuration_class: Class of the configuration object to be retrieved.
            metadata: Applicaton metadata.
            logger: Logger instance for this class.
        """
        self.metadata = metadata
        self.logger = logger
        self._configuration_class = configuration_class
        self.configuration = None

    @abstractmethod
    def get(self, verbose: bool = True) -> BaseConfiguration:
        """Retrieve the configuration.

        Args:
            verbose: Whether to log detailed information during retrieval.

        Returns:
            The parsed configuration object of `_configuration_class` type.
        """
        pass

    def _parse_configuration(self, configuration_json: dict, verbose=True):
        """Parse JSON configuration into a configuration object.

        Args:
            configuration_json: Dictionary containing the configuration data.
            verbose: Whether to log the parsed configuration.

        Returns:
            Parsed configuration object of `_configuration_class` type..
        """
        secrets_filepath = self._get_secrets_filepath()
        configuration = self._configuration_class.model_validate_json(
            configuration_json, context={"secrets_file": secrets_filepath}
        )
        configuration.metadata = self.metadata

        if verbose:
            self.logger.info(f"::Environment:{self.metadata.environment}")
            self.logger.info(configuration.model_dump_json(indent=4))

        return configuration

    def _get_secrets_filepath(self) -> str:
        """Get the path to the secrets file based on environment.

        Returns:
            Path to the secrets file.
        """
        return f"{OnPremConfigurationRetriever.CONFIGURATIONS_DIR}/secrets.{self.metadata.environment.value}.env"


class RemoteConfigurationRetriever(BaseConfigurationRetriever):
    """Configuration retriever for remote sources.

    Retrieves configuration from remote sources like config servers or cloud storage.
    Currently not implemented.
    """

    def get(self, verbose: bool = True) -> BaseConfiguration:
        """Retrieve configuration from a remote source.

        Args:
            verbose: Whether to log detailed information during retrieval.

        Raises:
            NotImplementedError: This functionality is not yet implemented.

        Returns:
            The configuration object.
        """
        raise NotImplementedError(
            "Remote configuration is not implemented yet."
        )


class OnPremConfigurationRetriever(BaseConfigurationRetriever):
    """Configuration retriever for on-premise file sources.

    Retrieves configurations from local JSON files.
    """

    def get(self, verbose: bool = True) -> BaseConfiguration:
        """Retrieve configuration from local files.

        This method implements caching to avoid re-reading configuration files.

        Args:
            verbose: Whether to log detailed information during retrieval.

        Returns:
            The parsed configuration object.
        """
        if not self.configuration:
            self.configuration = self._get(verbose)
        return self.configuration

    def _get(self, verbose) -> BaseConfiguration:
        """Internal method to retrieve and parse configuration.

        Args:
            verbose: Whether to log detailed information during retrieval.

        Returns:
            The parsed configuration object.
        """
        configuration_filepath = self._get_configuration_filepath()
        with open(configuration_filepath) as f:
            configuration_json = f.read()
            return self._parse_configuration(
                configuration_json=configuration_json, verbose=verbose
            )

    def _get_configuration_filepath(self) -> str:
        """Get the path to the configuration file based on environment.

        Returns:
            Path to the configuration JSON file.
        """
        return f"{OnPremConfigurationRetriever.CONFIGURATIONS_DIR}/configuration.{self.metadata.environment.value}.json"


class ConfiguratioRetriverRegistry:
    """Registry for configuration retrievers.

    Provides factory methods to get the appropriate configuration retriever based on context.
    """

    def get(on_prem: bool) -> BaseConfigurationRetriever:
        """Get the appropriate configuration retriever class.

        Args:
            on_prem: Whether to use on-premise configuration or remote.

        Returns:
            The appropriate configuration retriever class.
        """
        if on_prem:
            return OnPremConfigurationRetriever
        else:
            return RemoteConfigurationRetriever
