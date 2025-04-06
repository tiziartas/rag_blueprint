"""
This script is the entry point for the embedding process.
It initializes the embedding orchestrator and starts the embedding workflow.
To run the script, execute the following command from the root directory of the project:

> python src/embed.py
"""

import asyncio
import logging

from core.logger import LoggerConfiguration
from embedding.bootstrap.initializer import EmbeddingInitializer
from embedding.orchestrators.registry import EmbeddingOrchestratorRegistry
from embedding.vector_stores.core.exceptions import CollectionExistsException
from embedding.vector_stores.registry import VectorStoreValidatorRegistry


async def run(
    logger: logging.Logger = LoggerConfiguration.get_logger(__name__),
):
    """
    Execute the embedding process.

    Args:
        logger: Logger instance for logging messages
    """
    initializer = EmbeddingInitializer()
    configuration = initializer.get_configuration()

    vector_store = configuration.embedding.vector_store
    validator = VectorStoreValidatorRegistry.get(vector_store.name).create(
        vector_store
    )
    try:
        validator.validate()
    except CollectionExistsException as e:
        logger.info(
            f"Collection '{e.collection_name}' already exists. "
            "Skipping embedding process."
        )
        return

    logger.info("Starting embedding process.")
    orchestrator = EmbeddingOrchestratorRegistry.get(
        configuration.embedding.orchestrator_name
    ).create(configuration)

    await orchestrator.embed()
    logger.info("Embedding process finished.")


if __name__ == "__main__":
    asyncio.run(run())
