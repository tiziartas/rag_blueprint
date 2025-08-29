from typing import Type, Dict, List, Any, Iterator, Optional

from apiclient import APIClient, retry_request
from core.logger import LoggerConfiguration
from pydantic import BaseModel, ValidationError

from core import SingletonFactory
from extraction.datasources.hackernews.configuration import (
    HackerNewsDatasourceConfiguration,
)

class StoryItem(BaseModel):
    id: int
    title: str
    url: str | None
    score: int
    by: str
    time: int
    #descendants: Optional[int] = 0
    #kids: Optional[List[int]] = []

class HackerNewsClient(APIClient):
    """
    API Client for the Hacker News API.
    """
    BASE_URL = "https://hacker-news.firebaseio.com/v0"
    logger = LoggerConfiguration.get_logger(__name__)

    def safe_get(self, path: str) -> Optional[Any]:
        url = f"{self.BASE_URL}/{path.lstrip('/')}"
        """
        Perform a GET request, raise for HTTP errors, parse JSON.

        Args:
            path: endpoint path under BASE_URL, e.g. "GetTopStories" or
                  "GetItemStoreis/item_id>"

        Returns:
            List[int] or Dict[str, Any]

        """
        try:
            resp = self.get(url)
        except Exception as e:
            self.logger.warning(f"Failed to fetch data for {url}: {e}")
            return None
        
        try:
            resp.raise_for_status()
        except Exception as e:
            self.logger.error(f"HTTP error for {url}: {e}")
            return None
        
        result = resp.json()
        if result is None:
            self.logger.debug(f"No result found for {url}")
            return None

        return result
        
    def get_top_stories(self) -> List[int]:
        story_ids = self.safe_get("topstories.json")
        if story_ids is None:
            self.logger.warning("Failed to fetch top stories.")
            return []
        return story_ids

    def get_item(self, item_id: int) -> Dict[str, Any]:
        item = self.safe_get(f"item/{item_id}.json")
        if item is None:
            self.logger.warning(f"Failed to fetch item with ID {item_id}.")
            return {}
        return item
    
    @retry_request
    def get_top_stories_with_details(self) -> Iterator[StoryItem]:
        top_ids = self.get_top_stories()
        for story_id in top_ids:
            self.logger.info(f"Processing story {story_id}")
            story_data = self.get_item(story_id)
            if story_data:
                try:
                    yield StoryItem.model_validate(story_data)
                except ValidationError as e:
                    self.logger.warning(f"Failed to validate story {story_id}: {e}")

class HackerNewsClientFactory(SingletonFactory):
    """
    Factory for creating and managing Hacker News client instances.

    This factory ensures only one Hacker News client is created per configuration,
    following the singleton pattern provided by the parent SingletonFactory class.
    """

    _configuration_class: Type = HackerNewsDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: HackerNewsDatasourceConfiguration
    ) -> HackerNewsClient:
        """
        Creates a new Hacker News client instance using the provided configuration.

        Args:
            configuration: Configuration object containing Hacker News details

        Returns:
            A configured Hacker News client instance ready for API interactions.
        """
        return HackerNewsClient()
