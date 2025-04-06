from embedding.bootstrap.configuration.configuration import EmbedderName
from embedding.embedders.basic.embedder import BasicEmbedderFactory
from embedding.embedders.registry import EmbedderRegistry


def register() -> None:
    """
    Registers the basic embedder with the embedder registry.

    This function adds the BasicEmbedderFactory to the EmbedderRegistry
    under the BASIC embedder name, making it available for use
    throughout the application.
    """
    EmbedderRegistry.register(
        EmbedderName.BASIC,
        BasicEmbedderFactory,
    )
