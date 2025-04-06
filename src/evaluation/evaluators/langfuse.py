from math import isnan
from typing import Type

from llama_index.core.query_engine import CustomQueryEngine

from augmentation.components.query_engines.langfuse.query_engine import (
    SourceProcess,
)
from augmentation.components.query_engines.registry import QueryEngineRegistry
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
    """Evaluator for tracking RAG performance in Langfuse.

    Combines query engine execution with RAGAS evaluation and
    uploads results to Langfuse for monitoring.

    Attributes:
        query_engine: Engine for generating responses
        ragas_evaluator: Evaluator for quality metrics
        langfuse_dataset_service: Service for dataset access
        run_name: Name of evaluation run
        run_metadata: Additional run context
    """

    def __init__(
        self,
        query_engine: CustomQueryEngine,
        langfuse_dataset_service: LangfuseDatasetService,
        ragas_evaluator: RagasEvaluator,
        run_metadata: dict,
    ) -> None:
        """Initialize Langfuse evaluator.

        Args:
            query_engine: Engine for response generation
            langfuse_dataset_service: Dataset access service
            ragas_evaluator: Quality metrics evaluator
            run_metadata: Run context information
        """
        self.query_engine = query_engine
        self.ragas_evaluator = ragas_evaluator
        self.langfuse_dataset_service = langfuse_dataset_service
        self.run_name = run_metadata["build_name"]
        self.run_metadata = run_metadata

    def evaluate(self, dataset_name: str) -> None:
        """Evaluate dataset and record results in Langfuse.

        Args:
            dataset_name: Name of dataset to evaluate

        Note:
            Uploads scores for answer relevancy, context recall,
            faithfulness and harmfulness when available.
        """
        langfuse_dataset = self.langfuse_dataset_service.get_dataset(
            dataset_name
        )

        for item in langfuse_dataset.items:

            response = self.query_engine.query(
                str_or_query_bundle=item.input["query_str"],
                chainlit_message_id=None,
                source_process=SourceProcess.DEPLOYMENT_EVALUATION,
            ).get_response()

            scores = self.ragas_evaluator.evaluate(response=response, item=item)

            trace = self.query_engine.get_current_langfuse_trace()
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
    _configuration_class: Type = EvaluationConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: EvaluationConfiguration
    ) -> LangfuseEvaluator:
        query_engine = QueryEngineRegistry.get(
            configuration.augmentation.query_engine.name
        ).create(configuration)
        langfuse_dataset_service = LangfuseDatasetServiceFactory.create(
            configuration.augmentation.langfuse
        )
        ragas_evaluator = RagasEvaluatorFactory.create(configuration.evaluation)
        return LangfuseEvaluator(
            query_engine=query_engine,
            langfuse_dataset_service=langfuse_dataset_service,
            ragas_evaluator=ragas_evaluator,
            run_metadata={
                "build_name": configuration.metadata.build_name,
                "llm_configuration": configuration.augmentation.query_engine.synthesizer.llm.name,
                "judge_llm_configuration": configuration.evaluation.judge_llm.name,
            },
        )
