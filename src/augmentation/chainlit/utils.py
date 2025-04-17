from typing import List, Type

from chainlit import Message
from llama_index.core.base.response.schema import StreamingResponse
from llama_index.core.schema import NodeWithScore

from augmentation.bootstrap.configuration.chainlit_configuration import (
    ChainlitConfiguration,
)
from core.base_factory import SingletonFactory


class ChainlitUtils:
    """Utility class for handling conversation messages.

    Provides methods for managing welcome messages and reference handling in conversations.

    Attributes:
        REFERENCES_TEMPLATE: Template string for formatting references section.
    """

    REFERENCES_TEMPLATE = "\n\n**References**:\n" "{references}\n"

    def __init__(self, configuration: ChainlitConfiguration):
        """Initialize ChainlitUtils with configuration.

        Args:
            configuration (ChainlitConfiguration): Configuration containing settings
                                                  like welcome message.
        """
        self.configuration = configuration

    def get_welcome_message(self) -> Message:
        """Create and return a welcome message for the chat interface.

        Creates a Message object with content from the configuration's welcome_message
        to greet users when they start a conversation.

        Returns:
            Message: A chainlit Message object with the Assistant as author
                    and the welcome message as content.
        """
        return Message(
            author="Assistant", content=self.configuration.welcome_message
        )

    def add_references(
        self, message: Message, response: StreamingResponse
    ) -> None:
        """Append source references to a message from a streaming response.

        Takes a message object and a streaming response containing source nodes,
        then appends formatted references to the message content.

        Args:
            message (Message): The chainlit Message object to modify by adding references.
            response (StreamingResponse): A response object containing source_nodes
                                          with reference information.
        """
        message.content += self._get_references_str(response.source_nodes)

    def _get_references_str(self, nodes: List[NodeWithScore]) -> str:
        """Generate a formatted references section from source nodes.

        Processes a list of source nodes to create a deduplicated,
        formatted string of references.

        Args:
            nodes (List[NodeWithScore]): List of source nodes with relevance scores
                                         and metadata containing reference information.

        Returns:
            str: A formatted string containing unique references in the
                 structure defined by REFERENCES_TEMPLATE.
        """
        raw_references = [self._get_reference_str(node) for node in nodes]
        references = "\n".join(set(raw_references))
        return self.REFERENCES_TEMPLATE.format(references=references)

    def _get_reference_str(self, node: NodeWithScore) -> str:
        """Format a single node's reference as a markdown string.

        Extracts title and URL from a node's metadata and formats it
        as a markdown list item, with link formatting if a URL is available.

        Args:
            node (NodeWithScore): A source node containing metadata with
                                 title and optional URL information.

        Returns:
            str: A formatted markdown list item representing the reference,
                 with a clickable link if URL is available.
        """
        title = node.metadata.get("title")
        if not title:
            title = node.metadata.get("Title")

        url = node.metadata.get("url")

        if url:
            return "- [{}]({})".format(title, url)
        else:
            return f"- {title}"


class ChainlitUtilsFactory(SingletonFactory):
    """
    Factory class for creating ChainlitUtils instances.

    This class extends the Factory pattern to create instances of ChainlitUtils
    based on a given ChainlitConfiguration. It ensures that the configuration
    provided is of the correct type and handles the creation of new instances.

    Attributes:
        _configuration_class (Type): The expected type of configuration objects.
    """

    _configuration_class: Type = ChainlitConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: ChainlitConfiguration
    ) -> ChainlitUtils:
        """Create a new ChainlitUtils instance.

        Args:
            configuration (ChainlitConfiguration): Configuration object for ChainlitUtils.

        Returns:
            ChainlitUtils: A new instance of ChainlitUtils initialized with the given configuration.
        """
        return ChainlitUtils(configuration)
