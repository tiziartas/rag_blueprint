from typing import Type

from langfuse.client import Langfuse

from augmentation.bootstrap.configuration.langfuse_configuration import (
    LangfuseConfiguration,
)
from core import SingletonFactory


class LangfuseClientFactory(SingletonFactory):
    _configuration_class: Type = LangfuseConfiguration

    @classmethod
    def _create_instance(cls, configuration: LangfuseConfiguration) -> Langfuse:
        return Langfuse(
            secret_key=configuration.secrets.secret_key.get_secret_value(),
            public_key=configuration.secrets.public_key.get_secret_value(),
            host=configuration.url,
        )
