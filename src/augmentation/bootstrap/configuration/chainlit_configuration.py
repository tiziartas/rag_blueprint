from pydantic import Field

from core.base_configuration import BaseConfiguration


class ChainlitConfiguration(BaseConfiguration):
    """Configuration for Chainlit service.

    This class handles the configuration parameters needed to run
    a Chainlit service for the RAG application interface.
    """

    port: int = Field(8000, description="Port to run the chainlit service on.")
    welcome_message: str = Field(
        "Welcome to our Bavarian Beer Chat! 🍻 We're here to guide you through the rich tapestry of Bavarian beer culture. Whether you're curious about traditional brews, local beer festivals, or the history behind Bavaria's renowned beer purity law, you've come to the right place. Type your question below, and let's embark on this flavorful journey together. Prost!",
        description="Welcome message to display to users when they start a conversation.",
    )
