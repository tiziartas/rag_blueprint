from typing import Type

from core.base_factory import Factory
from core.logger import LoggerConfiguration
from extraction.datasources.hackernews.client import StoryItem
from extraction.datasources.hackernews.configuration import (
    HackerNewsDatasourceConfiguration,
)
from extraction.datasources.hackernews.document import HackerNewsDocument
from extraction.datasources.core.parser import BaseParser


class HackerNewsDatasourceParser(BaseParser[HackerNewsDocument]):
   
    logger = LoggerConfiguration.get_logger(__name__)

    def parse(self, story: StoryItem) -> HackerNewsDocument:
        """
        Parse content into a HackerNewsDocument object.

        Args:
            content: Raw response dict to be parsed

        Returns:
            Parsed document of type HackerNewsDocument
        """
        metadata = self._extract_metadata(story)
        return HackerNewsDocument(text=story.title, metadata=metadata)
    
    def _extract_metadata(self, story: StoryItem) -> dict:
        """
        Extract metadata from the response.

        Args:
            response: Raw response string

        Returns:
            Dictionary containing extracted metadata
        """    
        return {
            "id": story.id,
            "title": story.title,
            "url": story.url,
            "score": story.score,
            "by": story.by,
            "time": story.time,
        }


class HackerNewsDatasourceParserFactory(Factory):
    """
    Factory for creating instances of HackerNewsDatasourceParser.

    Creates and configures HackerNewsDatasourceParser objects according to
    the provided configuration.
    """

    _configuration_class: Type = HackerNewsDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: HackerNewsDatasourceConfiguration
    ) -> HackerNewsDatasourceParser:
        """
        Create an instance of HackerNewsDatasourceParser.

        Args:
            configuration: Configuration for the parser (not used in this implementation)

        Returns:
            An instance of HackerNewsDatasourceParser
        """
        return HackerNewsDatasourceParser()
