from enum import Enum
from typing import List, Type

from langfuse.client import StatefulTraceClient
from langfuse.llama_index.llama_index import LlamaIndexCallbackHandler
from llama_index.core.base.response.schema import RESPONSE_TYPE
from llama_index.core.callbacks import CallbackManager
from llama_index.core.postprocessor.types import BaseNodePostprocessor
from llama_index.core.query_engine import CustomQueryEngine
from llama_index.core.response_synthesizers import BaseSynthesizer
from llama_index.core.retrievers import BaseRetriever
from llama_index.core.schema import QueryBundle, QueryType
from pydantic import Field

from augmentation.bootstrap.configuration.configuration import (
    AugmentationConfiguration,
)
from augmentation.components.postprocessors.registry import (
    PostprocessorRegistry,
)
from augmentation.components.query_engines.langfuse.callback_manager import (
    LlamaIndexCallbackManagerFactory,
)
from augmentation.components.retrievers.registry import RetrieverRegistry
from augmentation.components.synthesizers.registry import SynthesizerRegistry
from core.base_factory import Factory


class SourceProcess(Enum):
    """Enumeration of possible query processing sources.

    Attributes:
        CHAT_COMPLETION: Query from interactive chat completion interface
        DEPLOYMENT_EVALUATION: Query from automated deployment testing and evaluation
    """

    CHAT_COMPLETION = 1
    DEPLOYMENT_EVALUATION = 2


class LangfuseQueryEngine(CustomQueryEngine):
    """Custom query engine implementing Retrieval-Augmented Generation (RAG).

    Coordinates retrieval, post-processing, and response generation for RAG workflow.
    Integrates with Langfuse for tracing and Chainlit for message tracking.

    Attributes:
        retriever: Component for retrieving relevant documents from vector store
        postprocessors: Sequential chain of document post-processors for refining results
        response_synthesizer: Component for generating coherent responses from retrieved context
        callback_manager: Manager for handling observability and tracing callbacks
        chainlit_tag_format: Format string for creating Chainlit message reference tags
    """

    retriever: BaseRetriever = Field(
        description="The retriever used to retrieve relevant nodes based on a given query."
    )
    postprocessors: List[BaseNodePostprocessor] = Field(
        description="The postprocessor used to process the retrieved nodes."
    )
    response_synthesizer: BaseSynthesizer = Field(
        description="The response synthesizer used to generate a response based on the retrieved nodes and the original query."
    )
    callback_manager: CallbackManager = Field(
        description="The callback manager used to handle callbacks."
    )
    chainlit_tag_format: str = Field(
        description="Format of the tag used to retrieve the trace by chainlit message id in Langfuse."
    )

    def query(
        self,
        str_or_query_bundle: QueryType,
        chainlit_message_id: str = None,
        source_process: SourceProcess = SourceProcess.CHAT_COMPLETION,
    ) -> RESPONSE_TYPE:
        """Process a query using RAG pipeline with Langfuse tracing.

        Args:
            str_or_query_bundle: Raw query string or structured query bundle
            chainlit_message_id: Optional ID for linking to Chainlit message in UI
            source_process: Context identifier indicating query's origin source

        Returns:
            RESPONSE_TYPE: Generated response from RAG pipeline with metadata
        """
        self._set_chainlit_message_id(
            message_id=chainlit_message_id, source_process=source_process
        )
        return super().query(str_or_query_bundle)

    async def aquery(
        self,
        str_or_query_bundle: QueryType,
        chainlit_message_id: str = None,
        source_process: SourceProcess = SourceProcess.CHAT_COMPLETION,
    ) -> RESPONSE_TYPE:
        """Asynchronously process a query using RAG pipeline with Langfuse tracing.

        Args:
            str_or_query_bundle: Raw query string or structured query bundle
            chainlit_message_id: Optional ID for linking to Chainlit message in UI
            source_process: Context identifier indicating query's origin source

        Returns:
            RESPONSE_TYPE: Generated response from RAG pipeline with metadata
        """
        self._set_chainlit_message_id(
            message_id=chainlit_message_id, source_process=source_process
        )
        return await super().aquery(str_or_query_bundle)

    def custom_query(self, query_str: str) -> RESPONSE_TYPE:
        """Execute custom RAG query processing pipeline with explicit control flow.

        Implements the core RAG workflow steps in sequence:
        1. Retrieve relevant documents using configured retriever
        2. Apply all registered post-processors to refine results
        3. Synthesize final response using the configured synthesizer

        Args:
            query_str: Raw query string to process

        Returns:
            Response object containing generated answer and metadata
        """
        nodes = self.retriever.retrieve(query_str)
        for postprocessor in self.postprocessors:
            nodes = postprocessor.postprocess_nodes(
                nodes, QueryBundle(query_str)
            )
        response_obj = self.response_synthesizer.synthesize(query_str, nodes)
        return response_obj

    def get_current_langfuse_trace(self) -> StatefulTraceClient:
        """Retrieve current Langfuse trace from registered callback handler.

        Searches through callback handlers to find active LlamaIndexCallbackHandler
        and extract its associated Langfuse trace for monitoring or annotation.

        Returns:
            StatefulTraceClient: Active Langfuse trace or None if not found
        """
        for handler in self.callback_manager.handlers:
            if isinstance(handler, LlamaIndexCallbackHandler):
                return handler.trace
        return None

    def set_session_id(self, session_id: str) -> None:
        """Set session ID for Langfuse tracing to group related queries.

        Updates the session identifier in all registered Langfuse callback handlers
        to enable session-level analytics and trace grouping.

        Args:
            session_id: Unique identifier for current user session
        """
        for handler in self.callback_manager.handlers:
            if isinstance(handler, LlamaIndexCallbackHandler):
                handler.session_id = session_id

    def _set_chainlit_message_id(
        self, message_id: str, source_process: SourceProcess
    ) -> None:
        """Configure Chainlit message tracking in Langfuse trace.

        Links the current Langfuse trace to a Chainlit message ID and tags
        with the processing source context for traceability in the Langfuse UI.

        Args:
            message_id: Chainlit message identifier to reference
            source_process: Source context enum categorizing the query origin
        """
        for handler in self.callback_manager.handlers:
            if isinstance(handler, LlamaIndexCallbackHandler):
                handler.set_trace_params(
                    tags=[
                        self.chainlit_tag_format.format(message_id=message_id),
                        source_process.name.lower(),
                    ]
                )


class LangfuseQueryEngineFactory(Factory):
    """Factory for creating configured LangfuseQueryEngine instances.

    Constructs and connects components needed for the RAG pipeline including:
    - Retriever for document fetching
    - Postprocessors for refining results
    - Response synthesizer for answer generation
    - Langfuse callback manager for observability
    """

    _configuration_class: Type = AugmentationConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: AugmentationConfiguration
    ) -> LangfuseQueryEngine:
        """Create and configure a LangfuseQueryEngine instance from configuration.

        Instantiates all RAG pipeline components based on configuration settings,
        connects them with a shared callback manager for tracing, and assembles
        them into a complete query engine.

        Args:
            configuration: Complete augmentation configuration containing
                           settings for all components

        Returns:
            LangfuseQueryEngine: Fully configured RAG query engine with tracing
        """
        query_engine_configuration = configuration.augmentation.query_engine
        synthesizer = SynthesizerRegistry.get(
            query_engine_configuration.synthesizer.name
        ).create(query_engine_configuration.synthesizer)
        retriever = RetrieverRegistry.get(
            query_engine_configuration.retriever.name
        ).create(configuration)
        postprocessors = [
            PostprocessorRegistry.get(postprocessor_configuration.name).create(
                postprocessor_configuration
            )
            for postprocessor_configuration in query_engine_configuration.postprocessors
        ]
        langfuse_callback_manager = LlamaIndexCallbackManagerFactory.create(
            configuration.augmentation.langfuse
        )

        retriever.callback_manager = langfuse_callback_manager
        synthesizer.callback_manager = langfuse_callback_manager
        for postprocessor in postprocessors:
            postprocessor.callback_manager = langfuse_callback_manager

        return LangfuseQueryEngine(
            retriever=retriever,
            postprocessors=postprocessors,
            response_synthesizer=synthesizer,
            callback_manager=langfuse_callback_manager,
            chainlit_tag_format=configuration.augmentation.langfuse.chainlit_tag_format,
        )
