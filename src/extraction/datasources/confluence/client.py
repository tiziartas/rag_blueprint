from typing import Type

from atlassian import Confluence

from core import SingletonFactory
from extraction.datasources.confluence.configuration import (
    ConfluenceDatasourceConfiguration,
)


class ConfluenceClientFactory(SingletonFactory):
    """
    Factory for creating and managing Confluence client instances.

    This factory ensures only one Confluence client is created per configuration,
    following the singleton pattern provided by the parent SingletonFactory class.
    """

    _configuration_class: Type = ConfluenceDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: ConfluenceDatasourceConfiguration
    ) -> Confluence:
        """
        Creates a new Confluence client instance using the provided configuration.

        Args:
            configuration: Configuration object containing Confluence connection details
                          including base URL, username, and password.

        Returns:
            A configured Confluence client instance ready for API interactions.
        """
        return Confluence(
            url=configuration.base_url,
            username=configuration.secrets.username.get_secret_value(),
            password=configuration.secrets.password.get_secret_value(),
        )
