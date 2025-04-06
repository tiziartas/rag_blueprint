"""
This script is used to evaluate RAG system using langfuse datasets. To add a new item to datasets, visit Langfuse UI.
Qdrant vector storage should be running with ready collection of embeddings.
To run the script execute the following command from the root directory of the project:

> python src/evaluate.py
"""

import logging

from core.logger import LoggerConfiguration
from evaluation.bootstrap.initializer import EvaluationInitializer
from evaluation.evaluators.langfuse import LangfuseEvaluatorFactory


def run(logger: logging.Logger = LoggerConfiguration.get_logger(__name__)):
    """Execute RAG system evaluation workflow.

    Args:
        injector: Dependency injection container

    Note:
        Evaluates both feedback and manual datasets
        Results are recorded in Langfuse
    """
    initializer = EvaluationInitializer()
    configuration = initializer.get_configuration()
    langfuse_evaluator = LangfuseEvaluatorFactory.create(configuration)

    logger.info(f"Evaluating {langfuse_evaluator.run_name}...")

    langfuse_evaluator.evaluate(
        dataset_name=configuration.augmentation.langfuse.datasets.feedback_dataset.name
    )
    langfuse_evaluator.evaluate(
        dataset_name=configuration.augmentation.langfuse.datasets.manual_dataset.name
    )

    logger.info(f"Evaluation complete for {configuration.metadata.build_name}.")


if __name__ == "__main__":
    run()
