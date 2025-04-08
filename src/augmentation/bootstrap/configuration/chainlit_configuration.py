from pydantic import BaseModel, Field


class ChainlitConfiguration(BaseModel):
    """Configuration for Chainlit service.

    This class handles the configuration parameters needed to run
    a Chainlit service for the RAG application interface.
    """

    port: int = Field(8000, description="Port to run the chainlit service on.")
