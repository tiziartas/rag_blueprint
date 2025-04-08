from typing import Any, Type

from chainlit.data.sql_alchemy import BaseDataLayer
from chainlit.types import Feedback

from augmentation.bootstrap.configuration.configuration import (
    _AugmentationConfiguration,
)
from augmentation.bootstrap.configuration.langfuse_configuration import (
    LangfuseDatasetConfiguration,
)
from augmentation.chainlit.feedback_service import (
    ChainlitFeedbackService,
    ChainlitFeedbackServiceFactory,
    LangfuseDatasetServiceFactory,
)
from augmentation.langfuse.dataset_service import LangfuseDatasetService
from core import Factory


class ChainlitService(BaseDataLayer):
    """Data layer implementation for Chainlit integration with Langfuse.

    Handles persistence of feedback and dataset management through Langfuse.
    """

    def __init__(
        self,
        langfuse_dataset_service: LangfuseDatasetService,
        feedback_service: ChainlitFeedbackService,
        manual_dataset: LangfuseDatasetConfiguration,
    ):
        """Initialize the Chainlit service.

        Args:
            langfuse_dataset_service: Service for managing Langfuse datasets.
            feedback_service: Service handling Chainlit feedback.
            manual_dataset: Configuration for manual dataset.
        """
        self.manual_dataset = manual_dataset
        self.feedback_service = feedback_service

        langfuse_dataset_service.create_if_does_not_exist(self.manual_dataset)

    async def upsert_feedback(self, feedback: Feedback) -> bool:
        """Upsert Chainlit feedback to Langfuse database.

        Processes user feedback from Chainlit UI and stores it in Langfuse for
        analysis and dataset management.

        Args:
            feedback: Feedback object containing user feedback details and metadata.

        Returns:
            bool: True if feedback was successfully upserted, False otherwise.
        """
        return await self.feedback_service.upsert(feedback)

    async def build_debug_url(self, *args: Any, **kwargs: Any) -> None:
        """Build a debug URL for Chainlit thread debugging.

        Not implemented in this integration.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        pass

    async def create_element(self, *args: Any, **kwargs: Any) -> None:
        """Create a UI element in Chainlit.

        Not implemented in this integration.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        pass

    async def create_step(self, *args: Any, **kwargs: Any) -> None:
        """Create a conversation step in Chainlit.

        Not implemented in this integration.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        pass

    async def create_user(self, *args: Any, **kwargs: Any) -> None:
        """Create a user record in Chainlit.

        Not implemented in this integration.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        pass

    async def delete_element(self, *args: Any, **kwargs: Any) -> None:
        """Delete a UI element from Chainlit.

        Not implemented in this integration.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        pass

    async def delete_feedback(self, *args: Any, **kwargs: Any) -> None:
        """Delete user feedback from storage.

        Not implemented in this integration.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        pass

    async def delete_step(self, *args: Any, **kwargs: Any) -> None:
        """Delete a conversation step from Chainlit.

        Not implemented in this integration.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        pass

    async def delete_thread(self, *args: Any, **kwargs: Any) -> None:
        """Delete a conversation thread from Chainlit.

        Not implemented in this integration.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        pass

    async def get_element(self, *args: Any, **kwargs: Any) -> None:
        """Retrieve a UI element from Chainlit.

        Not implemented in this integration.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        pass

    async def get_thread(self, *args: Any, **kwargs: Any) -> None:
        """Retrieve a conversation thread from Chainlit.

        Not implemented in this integration.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        pass

    async def get_thread_author(self, *args: Any, **kwargs: Any) -> None:
        """Retrieve the author of a conversation thread.

        Not implemented in this integration.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        pass

    async def get_user(self, *args: Any, **kwargs: Any) -> None:
        """Retrieve a user record from Chainlit.

        Not implemented in this integration.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        pass

    async def list_threads(self, *args: Any, **kwargs: Any) -> None:
        """List all conversation threads in Chainlit.

        Not implemented in this integration.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        pass

    async def update_step(self, *args: Any, **kwargs: Any) -> None:
        """Update a conversation step in Chainlit.

        Not implemented in this integration.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        pass

    async def update_thread(self, *args: Any, **kwargs: Any) -> None:
        """Update a conversation thread in Chainlit.

        Not implemented in this integration.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        pass


class ChainlitServiceFactory(Factory):
    """Factory for creating ChainlitService instances.

    Creates and configures ChainlitService instances using application configuration.

    Attributes:
        _configuration_class (Type): The configuration class used for creating
            ChainlitService instances. In this case, it is _AugmentationConfiguration.
    """

    _configuration_class: Type = _AugmentationConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: _AugmentationConfiguration
    ) -> ChainlitService:
        """Create a configured ChainlitService instance.

        Args:
            configuration: Application configuration containing Langfuse settings.

        Returns:
            ChainlitService: Configured service instance ready for use.
        """
        langfuse_dataset_service = LangfuseDatasetServiceFactory.create(
            configuration.langfuse
        )
        feedback_service = ChainlitFeedbackServiceFactory.create(configuration)
        manual_dataset = configuration.langfuse.datasets.manual_dataset
        return ChainlitService(
            langfuse_dataset_service=langfuse_dataset_service,
            feedback_service=feedback_service,
            manual_dataset=manual_dataset,
        )
