from typing import Type

from atlassian import Confluence

from core import SingletonFactory
from extraction.datasources.confluence.configuration import (
    ConfluenceDatasourceConfiguration,
)


class ConfluenceClientFactory(SingletonFactory):
    _configuration_class: Type = ConfluenceDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: ConfluenceDatasourceConfiguration
    ) -> Confluence:
        return Confluence(
            url=configuration.base_url,
            username=configuration.secrets.username.get_secret_value(),
            password=configuration.secrets.password.get_secret_value(),
        )
