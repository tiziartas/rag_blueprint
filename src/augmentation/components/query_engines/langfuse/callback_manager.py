from typing import Type

from langfuse.llama_index import LlamaIndexCallbackHandler
from llama_index.core.callbacks import CallbackManager

from augmentation.bootstrap.configuration.langfuse_configuration import (
    LangfuseConfiguration,
)
from core import Factory


class LlamaIndexCallbackManagerFactory(Factory):
    """Factory class for creating LlamaIndex callback managers with Langfuse integration.

    This factory creates a callback manager with a Langfuse handler to enable
    tracking and observability for LlamaIndex operations.

    Attributes:
        _configuration_class (Type): The configuration class used for creating
    """

    _configuration_class: Type = LangfuseConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: LangfuseConfiguration, session_id: str = ""
    ) -> LlamaIndexCallbackHandler:
        """Create a CallbackManager with a LlamaIndexCallbackHandler for Langfuse integration.

        This method creates a Langfuse callback handler using the provided configuration
        and wraps it in a CallbackManager.

        Args:
            configuration: Langfuse configuration containing API keys and URL
            session_id: Optional identifier for the session to group related traces

        Returns:
            A configured CallbackManager with the Langfuse callback handler
        """
        handler = LlamaIndexCallbackHandler(
            secret_key=configuration.secrets.secret_key.get_secret_value(),
            public_key=configuration.secrets.public_key.get_secret_value(),
            host=configuration.url,
            session_id=session_id,
        )
        return CallbackManager(handlers=[handler])
