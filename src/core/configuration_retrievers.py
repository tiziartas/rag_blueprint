import logging
from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel

from core.base_configuration import BaseConfiguration, MetadataConfiguration
from core.logger import LoggerConfiguration


class BaseConfigurationRetriever(ABC):

    CONFIGURATIONS_DIR = "configurations"

    def __init__(
        self,
        configuration_class: Type[BaseModel],
        metadata: MetadataConfiguration,
        logger: logging.Logger = LoggerConfiguration.get_logger(__name__),
    ):
        self.metadata = metadata
        self.logger = logger
        self._configuration_class = configuration_class
        self.configuration = None

    @abstractmethod
    def get(self, verbose=True) -> BaseConfiguration:
        pass

    def _parse_configuration(self, configuration_json: dict, verbose=True):
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
        return f"{OnPremConfigurationRetriever.CONFIGURATIONS_DIR}/secrets.{self.metadata.environment.value}.env"


class RemoteConfigurationRetriever(BaseConfigurationRetriever):

    def get(self, verbose=True) -> BaseConfiguration:
        raise NotImplementedError(
            "Remote configuration is not implemented yet."
        )


class OnPremConfigurationRetriever(BaseConfigurationRetriever):

    def get(self, verbose=True) -> BaseConfiguration:
        if not self.configuration:
            self.configuration = self._get(verbose)
        return self.configuration

    def _get(self, verbose) -> BaseConfiguration:
        configuration_filepath = self._get_configuration_filepath()
        with open(configuration_filepath) as f:
            configuration_json = f.read()
            return self._parse_configuration(
                configuration_json=configuration_json, verbose=verbose
            )

    def _get_configuration_filepath(self) -> str:
        """Get the configuration and secrets files from the command line arguments.

        Args:
            args: Parsed command line arguments

        Returns:
            Tuple[str, str]: Configuration and secrets filepaths
        """

        return f"{OnPremConfigurationRetriever.CONFIGURATIONS_DIR}/configuration.{self.metadata.environment.value}.json"


class ConfiguratioRetriverRegistry:

    def get(on_prem: bool) -> BaseConfigurationRetriever:
        if on_prem:
            return OnPremConfigurationRetriever
        else:
            return RemoteConfigurationRetriever
