from math import isnan
from typing import Type

from langfuse.model import DatasetStatus

from augmentation.components.chat_engines.langfuse.chat_engine import (
    LangfuseChatEngine,
    SourceProcess,
)
from augmentation.components.chat_engines.registry import ChatEngineRegistry
from augmentation.langfuse.dataset_service import (
    LangfuseDatasetService,
    LangfuseDatasetServiceFactory,
)
from core import Factory
from evaluation.bootstrap.configuration.configuration import (
    EvaluationConfiguration,
)
from evaluation.evaluators.ragas import RagasEvaluator, RagasEvaluatorFactory


class LangfuseEvaluator:
    """Evaluator that tracks RAG performance metrics in Langfuse.

    Integrates chat engine execution with RAGAS evaluation and
    publishes quality metrics to Langfuse for monitoring and analysis.
    """

    def __init__(
        self,
        chat_engine: LangfuseChatEngine,
        langfuse_dataset_service: LangfuseDatasetService,
        ragas_evaluator: RagasEvaluator,
        run_metadata: dict,
    ) -> None:
        """Initialize the Langfuse evaluator with required components.

        Args:
            chat_engine: The chat engine that will generate responses
            langfuse_dataset_service: Service to retrieve evaluation datasets
            ragas_evaluator: Component to calculate quality metrics
            run_metadata: Dictionary containing metadata about the evaluation run
        """
        self.chat_engine = chat_engine
        self.ragas_evaluator = ragas_evaluator
        self.langfuse_dataset_service = langfuse_dataset_service
        self.run_name = run_metadata["build_name"]
        self.run_metadata = run_metadata

    def evaluate(self, dataset_name: str) -> None:
        """Run evaluation on a dataset and record results in Langfuse.

        Processes each item in the dataset, generates responses using the chat engine,
        calculates evaluation metrics, and uploads all results to Langfuse for monitoring.

        Args:
            dataset_name: Identifier of the dataset to evaluate

        Note:
            Records scores for answer relevancy, context recall, faithfulness, and
            harmfulness metrics when they are available (not NaN values).
        """
        langfuse_dataset = self.langfuse_dataset_service.get_dataset(
            dataset_name
        )

        for item in langfuse_dataset.items:

            if item.status == DatasetStatus.ARCHIVED:
                continue

            response = self.chat_engine.chat(
                message=item.input["query_str"],
                chat_history=[],
                chainlit_message_id=None,
                source_process=SourceProcess.DEPLOYMENT_EVALUATION,
            )

            scores = self.ragas_evaluator.evaluate(response=response, item=item)

            trace = self.chat_engine.get_current_langfuse_trace()
            trace.update(output=response.response)
            item.link(
                trace_or_observation=trace,
                run_name=self.run_name,
                run_description="Deployment evaluation",
                run_metadata=self.run_metadata,
            )

            # TODO: How to handle NaNs?
            if not isnan(scores["answer_relevancy"]):
                trace.score(
                    name="Answer Relevancy", value=scores["answer_relevancy"]
                )
            if not isnan(scores["context_recall"]):
                trace.score(
                    name="Context Recall", value=scores["context_recall"]
                )
            if not isnan(scores["faithfulness"]):
                trace.score(name="Faithfulness", value=scores["faithfulness"])
            if not isnan(scores["harmfulness"]):
                trace.score(name="Harmfulness", value=scores["harmfulness"])


class LangfuseEvaluatorFactory(Factory):
    """Factory for creating LangfuseEvaluator instances.

    Creates properly configured evaluators based on the provided configuration.
    """

    _configuration_class: Type = EvaluationConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: EvaluationConfiguration
    ) -> LangfuseEvaluator:
        """Create a new LangfuseEvaluator instance.

        Args:
            configuration: Complete evaluation configuration containing
                           settings for the chat engine, datasets, and metrics

        Returns:
            A fully configured LangfuseEvaluator instance ready for evaluation
        """
        chat_engine = ChatEngineRegistry.get(
            configuration.augmentation.chat_engine.name
        ).create(configuration)
        langfuse_dataset_service = LangfuseDatasetServiceFactory.create(
            configuration.augmentation.langfuse
        )
        ragas_evaluator = RagasEvaluatorFactory.create(configuration.evaluation)
        return LangfuseEvaluator(
            chat_engine=chat_engine,
            langfuse_dataset_service=langfuse_dataset_service,
            ragas_evaluator=ragas_evaluator,
            run_metadata={
                "build_name": configuration.metadata.build_name,
                "llm_configuration": configuration.augmentation.chat_engine.llm.name,
                "judge_llm_configuration": configuration.evaluation.judge_llm.name,
            },
        )
