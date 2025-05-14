import logging
from typing import Type

from chainlit.types import Feedback
from langfuse import Langfuse
from langfuse.api.resources.commons.types.observations_view import (
    ObservationsView,
)
from langfuse.api.resources.commons.types.trace_with_details import (
    TraceWithDetails,
)

from augmentation.bootstrap.configuration.configuration import (
    _AugmentationConfiguration,
)
from augmentation.bootstrap.configuration.langfuse_configuration import (
    LangfuseDatasetConfiguration,
)
from augmentation.chainlit.exceptions import TraceNotFoundException
from augmentation.langfuse.client import LangfuseClientFactory
from augmentation.langfuse.dataset_service import (
    LangfuseDatasetService,
    LangfuseDatasetServiceFactory,
)
from core import Factory
from core.logger import LoggerConfiguration


class ChainlitFeedbackService:
    """Service for handling Chainlit feedback and Langfuse integration.

    This service processes user feedback from the Chainlit UI and integrates it with
    Langfuse for tracking and analysis. It associates feedback with traces in Langfuse,
    saves positive feedback examples to datasets, and provides mechanisms for retrieving
    relevant trace information.

    The service tracks feedback scores, comments, and message content, allowing for
    detailed analytics in the Langfuse UI and quality improvement of responses over time.

    Attributes:
        SCORE_NAME: The standardized name used for feedback scores in Langfuse.
    """

    SCORE_NAME = "User Feedback"

    def __init__(
        self,
        langfuse_dataset_service: LangfuseDatasetService,
        langfuse_client: Langfuse,
        feedback_dataset: LangfuseDatasetConfiguration,
        chainlit_tag_format: str,
        logger: logging.Logger = LoggerConfiguration.get_logger(__name__),
    ):
        """Initialize the ChainlitFeedbackService. Creates the feedback dataset if it doesn't exist.

        Args:
            langfuse_dataset_service: Service for creating and managing Langfuse datasets.
            langfuse_client: Client for interacting with the Langfuse API.
            feedback_dataset: Configuration for the dataset where positive feedback is stored.
            chainlit_tag_format: Format string for generating tags to retrieve traces by message ID.
            logger: Logger instance for recording service activities.
        """
        self.langfuse_dataset_service = langfuse_dataset_service
        self.langfuse_client = langfuse_client
        self.feedback_dataset = feedback_dataset
        self.chainlit_tag_format = chainlit_tag_format
        self.logger = logger

        self.langfuse_dataset_service.create_if_does_not_exist(feedback_dataset)

    async def upsert(self, feedback: Feedback) -> bool:
        """Process and store Chainlit feedback in Langfuse.

        Takes a feedback object from Chainlit, associates it with the appropriate trace in Langfuse,
        and performs two main actions:
        1. Records the feedback as a score on the trace
        2. For positive feedback, saves the trace data to the feedback dataset for future model training

        Args:
            feedback: Chainlit Feedback object containing user feedback value, optional comment,
                     and reference to the message being rated.

        Returns:
            bool: True if feedback was successfully processed and stored, False if an error occurred.
        """
        trace = None
        try:
            trace = self._fetch_trace(feedback.forId)

            if self._is_positive(feedback):
                self.logger.info(
                    f"Uploading trace {trace.id} to dataset {self.feedback_dataset.name}."
                )
                self._upload_trace_to_dataset(trace)

            self.langfuse_client.score(
                trace_id=trace.id,
                name=ChainlitFeedbackService.SCORE_NAME,
                value=feedback.value,
                comment=feedback.comment,
            )
            self.logger.info(
                f"Upserted feedback for {trace.id} trace with value {feedback.value}."
            )
            return True
        except Exception as e:
            trace_id = trace.id if trace else None
            self.logger.warning(
                f"Failed to upsert feedback for {trace_id} trace: {e}"
            )
            return False

    def _fetch_trace(self, message_id: str) -> TraceWithDetails:
        """Retrieve Langfuse trace associated with a Chainlit message ID.

        Uses the configured tag format to locate the trace related to a specific
        Chainlit message.

        Args:
            message_id: The unique identifier of the Chainlit message.

        Returns:
            TraceWithDetails: The complete trace data for the message.

        Raises:
            TraceNotFoundException: If no trace exists with the tag for this message ID.
        """
        response = self.langfuse_client.fetch_traces(
            tags=[self.chainlit_tag_format.format(message_id=message_id)]
        )
        trace = response.data[0] if response.data else None
        if trace is None:
            raise TraceNotFoundException(message_id)
        return trace

    def _upload_trace_to_dataset(self, trace: TraceWithDetails) -> None:
        """Save a trace to the feedback dataset for model improvement.

        Extracts relevant data from the trace including input query, retrieved nodes,
        templating information, and the final response, then creates a dataset item
        that can be used for model evaluation or fine-tuning.

        Args:
            trace: The trace containing the complete interaction details.
        """
        retrieve_observation = self._fetch_last_retrieve_observation(trace)
        last_templating_observation = self._fetch_last_templating_observation(
            trace
        )
        output_generation_observation = (
            self._fetch_pre_last_generation_observation(trace)
        )
        self.langfuse_client.create_dataset_item(
            dataset_name=self.feedback_dataset.name,
            input={
                "query_str": trace.input,
                "nodes": retrieve_observation.output.get("nodes"),
                "templating": last_templating_observation.input,
            },
            expected_output={
                "result": output_generation_observation.output["blocks"][0][
                    "text"
                ],
            },
            source_trace_id=trace.id,
            metadata={
                "generated_by": output_generation_observation.model,
            },
        )

    def _fetch_last_retrieve_observation(
        self, trace: TraceWithDetails
    ) -> ObservationsView:
        """Get the most recent retrieval observation from a trace.

        Retrieves information about the knowledge retrieval step in the RAG pipeline,
        including which nodes/documents were retrieved.

        Args:
            trace: The trace containing all observations.

        Returns:
            ObservationsView: The most recent retrieval observation, containing retrieved nodes.
        """
        retrieve_observations = self.langfuse_client.fetch_observations(
            trace_id=trace.id,
            name="retrieve",
        )
        return max(retrieve_observations.data, key=lambda x: x.createdAt)

    def _fetch_last_templating_observation(
        self, trace: TraceWithDetails
    ) -> ObservationsView:
        """Get the most recent templating observation from a trace.

        Retrieves information about how the prompt was constructed before being
        sent to the language model.

        Args:
            trace: The trace containing all observations.

        Returns:
            ObservationsView: The most recent templating observation, containing prompt construction details.
        """
        templating_observations = self.langfuse_client.fetch_observations(
            trace_id=trace.id,
            name="templating",
        )
        return max(templating_observations.data, key=lambda x: x.createdAt)

    def _fetch_pre_last_generation_observation(
        self, trace: TraceWithDetails
    ) -> ObservationsView:
        """Get the second most recent output observation from a trace.

        Retrieves information about the output generated by the language model,
        specifically the one before the last one.

        Args:
            trace: The trace containing all observations.

        Returns:
            ObservationsView: The second most recent output observation.
        """
        output_observations = self.langfuse_client.fetch_observations(
            trace_id=trace.id,
            type="GENERATION",
        )
        return sorted(output_observations.data, key=lambda x: x.createdAt)[-2]

    @staticmethod
    def _is_positive(feedback: Feedback) -> bool:
        """Determine if the feedback is positive.

        Classifies feedback as positive if its numeric value is greater than zero.
        Positive feedback is used to identify high-quality examples for the dataset.

        Args:
            feedback: The feedback object containing the user's rating.

        Returns:
            bool: True if the feedback value is positive (greater than 0), False otherwise.
        """
        return feedback.value > 0


class ChainlitFeedbackServiceFactory(Factory):
    """Factory for creating ChainlitFeedbackService instances.

    This factory creates properly configured ChainlitFeedbackService instances using
    the application configuration. It handles initializing dependencies like the
    Langfuse client and dataset service.
    """

    _configuration_class: Type = _AugmentationConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: _AugmentationConfiguration
    ) -> ChainlitFeedbackService:
        """Create a new ChainlitFeedbackService instance.

        Creates and configures a feedback service with the proper Langfuse client,
        dataset service, and configuration settings.

        Args:
            configuration: Application configuration containing Langfuse settings.

        Returns:
            ChainlitFeedbackService: A fully configured feedback service instance.
        """
        langfuse_client = LangfuseClientFactory.create(configuration.langfuse)
        langfuse_dataset_service = LangfuseDatasetServiceFactory.create(
            configuration.langfuse
        )
        feedback_dataset = configuration.langfuse.datasets.feedback_dataset
        chainlit_tag_format = configuration.langfuse.chainlit_tag_format
        return ChainlitFeedbackService(
            langfuse_client=langfuse_client,
            langfuse_dataset_service=langfuse_dataset_service,
            feedback_dataset=feedback_dataset,
            chainlit_tag_format=chainlit_tag_format,
        )
