import asyncio
import logging

from core.logger import LoggerConfiguration
from embedding.bootstrap.initializer import EmbeddingInitializer
from embedding.orchestrators.registry import EmbeddingOrchestratorRegistry


async def run(
    logger: logging.Logger = LoggerConfiguration.get_logger(__name__),
):
    initializer = EmbeddingInitializer()
    configuration = initializer.get_configuration()

    logger.info("Starting embedding process.")
    orchestrator = EmbeddingOrchestratorRegistry.get(
        configuration.embedding.orchestrator_name
    ).create(configuration)

    await orchestrator.embed()
    logger.info("Embedding process finished.")


if __name__ == "__main__":
    asyncio.run(run())
