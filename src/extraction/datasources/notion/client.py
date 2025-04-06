from typing import Type

from notion_client import Client

from core.base_factory import SingletonFactory
from extraction.datasources.notion.configuration import (
    NotionDatasourceConfiguration,
)


class NotionClientFactory(SingletonFactory):
    """Factory for creating and managing Notion API client instances.

    This singleton factory ensures that only one Notion client instance is created
    for a specific configuration, promoting resource efficiency and consistency.
    Client instances are created using the Notion API authentication token
    from the provided configuration.

    The factory follows the singleton pattern to prevent multiple instantiations
    of clients with identical configurations.

    Attributes:
        _configuration_class: Type of configuration object used to create the client
    """

    _configuration_class: Type = NotionDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: NotionDatasourceConfiguration
    ) -> Client:
        """Create a new instance of the Notion API client.

        This method extracts the API token from the provided configuration's
        secrets and uses it to authenticate a new Notion client.

        Args:
            configuration: Configuration object containing Notion API credentials
                           and other settings.

        Returns:
            A configured Notion API client instance ready for making API calls.
        """
        return Client(auth=configuration.secrets.api_token.get_secret_value())
