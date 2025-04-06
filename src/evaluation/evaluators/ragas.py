from typing import Callable, Type

from datasets import Dataset
from langfuse.client import DatasetItemClient
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.base.llms.base import BaseLLM
from llama_index.core.base.response.schema import Response
from pandas import Series
from ragas.embeddings import LlamaIndexEmbeddingsWrapper
from ragas.evaluation import evaluate as ragas_evaluate
from ragas.llms import LlamaIndexLLMWrapper
from ragas.metrics import answer_relevancy, context_recall, faithfulness
from ragas.metrics.critique import harmfulness

from augmentation.components.llms.registry import LLMRegistry
from core import Factory
from embedding.embedding_models.registry import EmbeddingModelRegistry
from evaluation.bootstrap.configuration.configuration import (
    _EvaluationConfiguration,
)


class RagasEvaluator:
    """Evaluator for RAG system quality using RAGAS.

    Wraps LlamaIndex LLM and embedding models for use with RAGAS
    evaluation framework. Supports multiple evaluation metrics.

    Attributes:
        judge_llm: Wrapped LLM for evaluations
        embedding_model: Wrapped embeddings for metrics
        evaluator_function: Function to run evaluations
        metrics: List of RAGAS metrics to evaluate
    """

    def __init__(
        self,
        judge_llm: BaseLLM,
        judge_embedding_model: BaseEmbedding,
        evaluator_function: Callable = ragas_evaluate,
    ) -> None:
        """Initialize RAGAS evaluator with models.

        Args:
            judge_llm: LLM for evaluation judgments
            embedding_model: Model for embedding comparisons
            evaluator_function: Optional custom evaluation function
        """
        self.judge_llm = LlamaIndexLLMWrapper(judge_llm)
        self.judge_embedding_model = LlamaIndexEmbeddingsWrapper(
            judge_embedding_model
        )
        self.evaluator_function = evaluator_function

        self.metrics = [
            answer_relevancy,
            faithfulness,
            harmfulness,
            context_recall,
        ]

    def evaluate(self, response: Response, item: DatasetItemClient) -> Series:
        """Evaluate response quality using RAGAS metrics.

        Args:
            response: Query response to evaluate
            item: Dataset item containing ground truth

        Returns:
            Series: Scores for each metric
        """
        dataset = Dataset.from_dict(
            {
                "question": [item.input["query_str"]],
                "contexts": [[n.node.text for n in response.source_nodes]],
                "answer": [response.response],
                "ground_truth": [item.expected_output["result"]],
            }
        )
        return (
            self.evaluator_function(
                metrics=self.metrics,
                dataset=dataset,
                llm=self.judge_llm,
                embeddings=self.judge_embedding_model,
            )
            .to_pandas()
            .iloc[0]
        )


class RagasEvaluatorFactory(Factory):
    _configuration_class: Type = _EvaluationConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: _EvaluationConfiguration
    ) -> RagasEvaluator:
        judge_llm = LLMRegistry.get(configuration.judge_llm.provider).create(
            configuration.judge_llm
        )
        judge_embedding_model = EmbeddingModelRegistry.get(
            configuration.judge_embedding_model.provider
        ).create(configuration.judge_embedding_model)
        return RagasEvaluator(
            judge_llm=judge_llm, judge_embedding_model=judge_embedding_model
        )
