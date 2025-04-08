from typing import Type

from langfuse.client import Langfuse

from augmentation.bootstrap.configuration.langfuse_configuration import (
    LangfuseConfiguration,
)
from core import SingletonFactory


class LangfuseClientFactory(SingletonFactory):
    """
    Factory class for creating and managing Langfuse client instances.

    This class implements the Singleton pattern through inheriting from SingletonFactory,
    ensuring only one Langfuse client instance exists throughout the application.

    Attributes:
        _configuration_class (Type): The configuration class used for creating
            Langfuse client instances. In this case, it is LangfuseConfiguration.
    """

    _configuration_class: Type = LangfuseConfiguration

    @classmethod
    def _create_instance(cls, configuration: LangfuseConfiguration) -> Langfuse:
        """
        Creates a new Langfuse client instance.

        Args:
            configuration (LangfuseConfiguration): Configuration object containing
                Langfuse API credentials and URL settings.

        Returns:
            Langfuse: A configured Langfuse client instance ready for use with the
                provided credentials and host.
        """
        return Langfuse(
            secret_key=configuration.secrets.secret_key.get_secret_value(),
            public_key=configuration.secrets.public_key.get_secret_value(),
            host=configuration.url,
        )
