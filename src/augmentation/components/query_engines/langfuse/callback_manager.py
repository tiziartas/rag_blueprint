from typing import Type

from langfuse.llama_index import LlamaIndexCallbackHandler
from llama_index.core.callbacks import CallbackManager

from augmentation.bootstrap.configuration.langfuse_configuration import (
    LangfuseConfiguration,
)
from core import Factory


class LlamaIndexCallbackManagerFactory(Factory):
    _configuration_class: Type = LangfuseConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: LangfuseConfiguration, session_id: str = ""
    ) -> LlamaIndexCallbackHandler:
        handler = LlamaIndexCallbackHandler(
            secret_key=configuration.secrets.secret_key.get_secret_value(),
            public_key=configuration.secrets.public_key.get_secret_value(),
            host=configuration.url,
            session_id=session_id,
        )
        return CallbackManager(handlers=[handler])
