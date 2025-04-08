import logging
from typing import Type

from langfuse.api.resources.commons.errors.not_found_error import NotFoundError
from langfuse.client import DatasetClient, Langfuse

from augmentation.bootstrap.configuration.langfuse_configuration import (
    LangfuseConfiguration,
    LangfuseDatasetConfiguration,
)
from augmentation.langfuse.client import LangfuseClientFactory
from core import Factory
from core.logger import LoggerConfiguration


class LangfuseDatasetService:
    """Service for managing Langfuse datasets.

    This service provides methods to create, manage, and retrieve datasets within
    the Langfuse platform. It handles the communication with the Langfuse API for
    all dataset-related operations.
    """

    def __init__(
        self,
        langfuse_client: Langfuse,
        logger: logging.Logger = LoggerConfiguration.get_logger(__name__),
    ):
        """Initialize the Langfuse dataset service.

        Args:
            langfuse_client: Authenticated client for Langfuse API interactions.
            logger: Logger instance for recording operations. Defaults to module logger.
        """
        self.langfuse_client = langfuse_client
        self.logger = logger

    def create_if_does_not_exist(
        self, dataset: LangfuseDatasetConfiguration
    ) -> None:
        """Create a dataset in Langfuse if it doesn't already exist.

        Checks if a dataset with the specified name exists in Langfuse.
        If not found, creates a new dataset with the provided configuration.

        Args:
            dataset: Configuration object containing dataset name, description,
                    and metadata for creation.

        Note:
            The NotFoundError exception from Langfuse is caught and used as
            an indicator to create a new dataset, but is still logged due to
            Langfuse implementation details.
        """
        try:
            self.langfuse_client.get_dataset(dataset.name)
            self.logger.info(f"Dataset {dataset.name} exists.")
        except NotFoundError:
            self.logger.info(
                f"Dataset {dataset.name} does not exist. Creating..."
            )
            self.langfuse_client.create_dataset(
                name=dataset.name,
                description=dataset.description,
                metadata=dataset.metadata,
            )

    def get_dataset(self, dataset_name: str) -> DatasetClient:
        """Retrieve a dataset client by name.

        Provides a client instance for interacting with a specific dataset
        in the Langfuse platform.

        Args:
            dataset_name: The unique name identifier of the dataset to retrieve.

        Returns:
            DatasetClient: A client object for performing operations on the
                          specified dataset (such as adding examples, querying data).

        Raises:
            NotFoundError: If a dataset with the specified name doesn't exist.
        """
        return self.langfuse_client.get_dataset(dataset_name)


class LangfuseDatasetServiceFactory(Factory):
    """Factory for creating LangfuseDatasetService instances.

    Creates and configures LangfuseDatasetService instances with the appropriate
    client based on provided configuration.

    Attributes:
        _configuration_class: The configuration class type used by this factory.
    """

    _configuration_class: Type = LangfuseConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: LangfuseConfiguration
    ) -> LangfuseDatasetService:
        """Create a configured LangfuseDatasetService instance.

        Args:
            configuration: The Langfuse configuration containing API credentials
                          and other settings.

        Returns:
            A fully initialized LangfuseDatasetService instance with an authenticated client.
        """
        client = LangfuseClientFactory.create(configuration)
        return LangfuseDatasetService(client)
