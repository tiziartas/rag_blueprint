from typing import Type

from notion_client import Client

from core.base_factory import SingletonFactory
from extraction.datasources.notion.configuration import (
    NotionDatasourceConfiguration,
)


class NotionClientFactory(SingletonFactory):
    """Singleton factory for creating Notion client instances.

    This class ensures that only one instance of the Notion client is created
    and reused across the application. It provides a method to get the client
    instance, which is initialized with the provided API key.

    Attributes:
        _configuration_class (NotionDatasourceConfiguration): The configuration
            class used to create the Notion client instance.
    """

    _configuration_class: Type = NotionDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: NotionDatasourceConfiguration
    ) -> Client:
        return Client(auth=configuration.secrets.api_token.get_secret_value())
