import logging
from typing import AsyncIterator

from core import Factory
from core.logger import LoggerConfiguration
from extraction.datasources.bundestag.client import (
    BundestagMineClient,
    BundestagMineClientFactory,
)
from extraction.datasources.bundestag.configuration import (
    BundestagMineDatasourceConfiguration,
)
from extraction.datasources.core.reader import BaseReader


class BundestagMineDatasourceReader(BaseReader):
    """Reader for extracting speeches from the BundestagMine API.

    Implements document extraction from the Bundestag speeches.
    """

    def __init__(
        self,
        configuration: BundestagMineDatasourceConfiguration,
        client: BundestagMineClient,
        logger: logging.Logger = LoggerConfiguration.get_logger(__name__),
    ):
        """Initialize the BundestagMine reader.

        Args:
            configuration: Settings for BundestagMine access and export limits
            client: Client for BundestagMine API interactions
            logger: Logger instance for recording operation information
        """
        super().__init__()
        self.export_limit = configuration.export_limit
        self.client = client
        self.logger = logger

    async def read_all_async(
        self,
    ) -> AsyncIterator[dict]:
        """Asynchronously fetch all speeches from BundestagMine.

        Yields each speech as a dictionary containing its content and metadata.

        Returns:
            AsyncIterator[dict]: An async iterator of page dictionaries containing
            content and metadata such as text, speaker data, and last update information
        """
        self.logger.info(
            f"Fetching speeches from BundestagMine with limit {self.export_limit}"
        )
        speech_iterator = self.client.fetch_all_speeches()
        yield_counter = 0

        for speech in speeches:
            speech_limit = (
                self.export_limit - yield_counter
                if self.export_limit is not None
                else None
            )
            if speech_limit is not None and speech_limit <= 0:
                break

            yield_counter += 1
            yield speech


class BundestagMineDatasourceReaderFactory(Factory):
    """Factory for creating BundestagMine reader instances.

    Creates and configures BundestagMineDatasourceReader objects with appropriate
    clients based on the provided configuration.
    """

    _configuration_class = BundestagMineDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: BundestagMineDatasourceConfiguration
    ) -> BundestagMineDatasourceReader:
        """Creates a configured BundestagMine reader instance.

        Initializes the BundestagMine client and reader with the given configuration
        settings for credentials, URL, and export limits.

        Args:
            configuration: BundestagMine connection and access settings

        Returns:
            BundestagMineDatasourceReader: Fully configured reader instance
        """
        client = BundestagMineClientFactory.create(configuration)
        return BundestagMineDatasourceReader(
            configuration=configuration,
            client=client,
        )
