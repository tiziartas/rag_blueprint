from pydantic import Field

from core.base_configuration import BaseConfiguration


class ChainlitConfiguration(BaseConfiguration):
    """Configuration for Chainlit service.

    This class handles the configuration parameters needed to run
    a Chainlit service for the RAG application interface.
    """

    port: int = Field(8000, description="Port to run the chainlit service on.")
    disclaimer_title: str = Field(
        "Hacker News Chat",
        description="Title of the disclaimer message to be displayed.",
    )
    disclaimer_text: str = Field(
        "This content is AI-generated and may contain inaccuracies. Please verify any critical information independently. Additional details, including imprint and privacy policy information, can be found in the Readme file located a the top-right corner of the page.",
        description="Disclaimer text to be displayed to users.",
    )
    welcome_message: str = Field(
        "Welcome Pirate! You can retrive information from the top daily stories of Hacker News, Type your question below",
        description="Welcome message to display to users when they start a conversation.",
    )
