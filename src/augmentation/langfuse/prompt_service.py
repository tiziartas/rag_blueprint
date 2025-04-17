from typing import Type

from langfuse.client import Langfuse

from augmentation.bootstrap.configuration.langfuse_configuration import (
    LangfuseConfiguration,
)
from augmentation.langfuse.client import LangfuseClientFactory
from core.base_factory import Factory
from core.logger import LoggerConfiguration


class LangfusePromptService:

    def __init__(
        self, client: Langfuse, logger=LoggerConfiguration.get_logger(__name__)
    ):
        """
        Initializes the LangfusePromptService with a Langfuse client and a logger.

        Args:
            client (Langfuse): The Langfuse client instance.
            logger (Logger): The logger instance.
        """
        self.client = client
        self.logger = logger

    def create_prompt_if_not_exists(
        self,
        prompt_name: str,
        prompt_template: str,
    ) -> None:
        """
        Creates a new prompt in Langfuse if it does not already exist.

        Args:
            prompt_name (str): The name of the prompt.
            prompt_template (str): The template of the prompt.
        """
        if self.prompt_exists(prompt_name):
            return

        self.logger.info(f"Creating {prompt_name} prompt in Langfuse")
        self.client.create_prompt(
            name=prompt_name, prompt=prompt_template, labels=["production"]
        )

    def prompt_exists(
        self,
        prompt_name: str,
    ) -> bool:
        """
        Checks if a prompt exists in Langfuse.

        Args:
            prompt_name (str): The name of the prompt.

        Returns:
            bool: True if the prompt exists, False otherwise.
        """
        try:
            self.client.get_prompt(prompt_name)
            return True
        except Exception:
            return False

    def get_prompt_template(self, prompt_name: str) -> str:
        """
        Retrieves the prompt template from Langfuse.

        Args:
            prompt_name (str): The name of the prompt.

        Returns:
            str: The prompt template.
        """
        prompt = self.client.get_prompt(prompt_name)
        return prompt.prompt


class LangfusePromptServiceFactory(Factory):
    """
    Factory class for creating and managing Langfuse prompt service instances.

    This class implements the Singleton pattern through inheriting from Factory,
    ensuring only one Langfuse prompt service instance exists throughout the application.

    Attributes:
        _configuration_class (Type): The configuration class used for creating
            Langfuse prompt service instances. In this case, it is LangfuseConfiguration.
    """

    _configuration_class: Type = LangfuseConfiguration

    @classmethod
    def _create_instance(cls, configuration: LangfuseConfiguration) -> Langfuse:
        """
        Creates a new Langfuse prompt service instance.

        Args:
            configuration (LangfuseConfiguration): Configuration object containing
                Langfuse API credentials and URL settings.

        Returns:
            LangfusePromptService: A configured Langfuse prompt service instance ready for use with the
                provided credentials and host.
        """
        client = LangfuseClientFactory.create(configuration)
        return LangfusePromptService(client=client)
