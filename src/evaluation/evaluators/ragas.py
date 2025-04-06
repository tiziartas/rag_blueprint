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
    """Evaluator for RAG system quality using RAGAS framework.

    Provides automatic evaluation of RAG pipeline quality using multiple
    metrics from the RAGAS evaluation framework. Evaluates answer relevancy,
    factual consistency (faithfulness), harmfulness, and source context recall.
    """

    def __init__(
        self,
        judge_llm: BaseLLM,
        judge_embedding_model: BaseEmbedding,
        evaluator_function: Callable = ragas_evaluate,
    ) -> None:
        """Initialize RAGAS evaluator with required models and configuration.

        Args:
            judge_llm: LlamaIndex LLM used to evaluate response quality
            judge_embedding_model: Embedding model for semantic comparisons
            evaluator_function: Function that runs the evaluation pipeline,
                defaults to the standard RAGAS evaluate function
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
        """Evaluate a RAG response against multiple quality metrics.

        Calculates RAGAS evaluation metrics comparing the response to ground truth
        and source contexts. Creates a temporary dataset structure needed for
        RAGAS evaluation framework.

        Args:
            response: LlamaIndex response object containing the generated answer
                and source nodes used for retrieval
            item: Langfuse dataset item containing the original query and
                expected ground truth answer

        Returns:
            Series: Pandas Series containing individual scores for each metric
                (answer relevancy, faithfulness, harmfulness, context recall)
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
    """Factory for creating configured RagasEvaluator instances.

    Creates RagasEvaluator objects based on provided configuration,
    handling the initialization of required LLM and embedding models.

    Attributes:
        _configuration_class: Configuration class type used for validation
    """

    _configuration_class: Type = _EvaluationConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: _EvaluationConfiguration
    ) -> RagasEvaluator:
        """Create and initialize a RagasEvaluator with configured models.

        Initializes judge LLM and embedding models according to configuration
        specifications, then creates a RagasEvaluator with those models.

        Args:
            configuration: Evaluation configuration object containing model
                specifications for the judge LLM and embedding model

        Returns:
            RagasEvaluator: Fully initialized evaluator ready to assess RAG responses
        """
        judge_llm = LLMRegistry.get(configuration.judge_llm.provider).create(
            configuration.judge_llm
        )
        judge_embedding_model = EmbeddingModelRegistry.get(
            configuration.judge_embedding_model.provider
        ).create(configuration.judge_embedding_model)
        return RagasEvaluator(
            judge_llm=judge_llm, judge_embedding_model=judge_embedding_model
        )
