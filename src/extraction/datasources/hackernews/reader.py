import logging
from typing import AsyncIterator

from core import Factory
from core.logger import LoggerConfiguration
from extraction.datasources.hackernews.client import (
    HackerNewsClient,
    HackerNewsClientFactory,
)
from extraction.datasources.hackernews.configuration import (
    HackerNewsDatasourceConfiguration,
)
from extraction.datasources.core.reader import BaseReader


class HackerNewsDatasourceReader(BaseReader):
    """Reader for extracting stories from the Hacker News API.

    Implements document extraction from the Hacker Story 
    """

    def __init__(
        self,
        configuration: HackerNewsDatasourceConfiguration,
        client: HackerNewsClient,
        logger: logging.Logger = LoggerConfiguration.get_logger(__name__),
    ):
        """Initialize the HackerNews reader.

        Args:
            configuration: Settings for HackerNews access and export limits
            client: Client for HackerNews API interactions
            logger: Logger instance for recording operation information
        """
        super().__init__()
        self.export_limit = configuration.export_limit
        self.client = client
        self.logger = logger

    async def read_all_async(
        self,
    ) -> AsyncIterator[dict]:
        """Asynchronously fetch top stories from Hacker News.

        Yields each stories as a dictionary containing its content and metadata.

        Returns:
            AsyncIterator[dict]: An async iterator of page dictionaries containing
            content and metadata 
        """
        self.logger.info(
            f"Reading stories from Hacker News with limit {self.export_limit}"
        )
        stories_iterator = self.client.get_top_stories_with_details()
        yield_counter = 0

        for story in stories_iterator:
            if self._limit_reached(yield_counter, self.export_limit):
                return

            self.logger.info(
                f"Fetched Hacker News story {yield_counter}/{self.export_limit}."
            )
            yield_counter += 1
            yield story



class HackerNewsDatasourceReaderFactory(Factory):
    """Factory for creating Hacker News reader instances.

    Creates and configures HackerNewsDatasourceReader objects with appropriate
    clients based on the provided configuration.
    """

    _configuration_class = HackerNewsDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: HackerNewsDatasourceConfiguration
    ) -> HackerNewsDatasourceReader:
        """Creates a configured Hacker News reader instance.

        Initializes the Hacker News client and reader with the given configuration
        settings for credentials, URL, and export limits.

        Args:
            configuration: Hacker News connection and access settings

        Returns:
            HackerNewsDatasourceReader: Fully configured reader instance
        """
        client = HackerNewsClientFactory.create(configuration)
        return HackerNewsDatasourceReader(
            configuration=configuration,
            client=client,
        )
