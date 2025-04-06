from embedding.bootstrap.configuration.configuration import EmbedderName
from embedding.embedders.basic.embedder import BasicEmbedderFactory
from embedding.embedders.registry import EmbedderRegistry


def register() -> None:
    EmbedderRegistry.register(
        EmbedderName.BASIC,
        BasicEmbedderFactory,
    )
