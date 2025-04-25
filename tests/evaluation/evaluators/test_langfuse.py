import sys

sys.path.append("./src")

from typing import List
from unittest.mock import Mock

import numpy as np
import pytest
from langfuse.client import (
    DatasetClient,
    DatasetItemClient,
    StatefulTraceClient,
)
from llama_index.core.chat_engine.types import AgentChatResponse

from augmentation.components.chat_engines.langfuse.chat_engine import (
    LangfuseChatEngine,
    SourceProcess,
)
from augmentation.langfuse.dataset_service import LangfuseDatasetService
from evaluation.evaluators.langfuse import LangfuseEvaluator
from evaluation.evaluators.ragas import RagasEvaluator


class Fixtures:

    def __init__(self):
        self.dataset_name: str = None
        self.dataset: DatasetClient = None
        self.items: List[DatasetItemClient] = []
        self.response: AgentChatResponse = None
        self.trace: StatefulTraceClient = None
        self.scores: dict = {}

    def with_dataset(self) -> "Fixtures":
        self.dataset_name = "dataset_name"
        self.dataset = Mock(spec=DatasetClient)
        self.dataset.items = self.items
        return self

    def with_items(self, number_of_items: int) -> "Fixtures":
        self.items = [self._create_item() for _ in range(number_of_items)]
        return self

    def with_response(self) -> "Fixtures":
        self.response = Mock(spec=AgentChatResponse)
        self.response.response = "response"
        return self

    def with_trace(self) -> "Fixtures":
        self.trace = Mock(spec=StatefulTraceClient)
        return self

    def with_scores(self, scores: dict) -> "Fixtures":
        self.scores = scores
        return self

    def _create_item(self) -> DatasetItemClient:
        item = Mock(spec=DatasetItemClient)
        item.input = {"query_str": "query"}
        item.status = "active"
        return item


class Arrangements:

    def __init__(self, fixtures: Fixtures) -> None:
        self.fixtures = fixtures

        self.chat_engine: LangfuseChatEngine = Mock(spec=LangfuseChatEngine)
        self.langfuse_dataset_service: LangfuseDatasetService = Mock(
            spec=LangfuseDatasetService
        )
        self.ragas_evaluator: RagasEvaluator = Mock(spec=RagasEvaluator)
        self.run_metadata = {"build_name": "build_name"}
        self.service = LangfuseEvaluator(
            chat_engine=self.chat_engine,
            langfuse_dataset_service=self.langfuse_dataset_service,
            ragas_evaluator=self.ragas_evaluator,
            run_metadata=self.run_metadata,
        )

    def on_langfuse_dataset_service_get_dataset_return_dataset(
        self,
    ) -> "Arrangements":
        self.langfuse_dataset_service.get_dataset.return_value = (
            self.fixtures.dataset
        )
        return self

    def on_chat_engine_chat_return_response(self) -> "Arrangements":
        self.chat_engine.chat.return_value = self.fixtures.response
        return self

    def on_ragas_evaluator_evaluate_return_scores(self) -> "Arrangements":
        self.ragas_evaluator.evaluate.return_value = self.fixtures.scores
        return self

    def on_chat_engine_get_current_langfuse_trace_return_trace(
        self,
    ) -> "Arrangements":
        self.chat_engine.get_current_langfuse_trace.return_value = (
            self.fixtures.trace
        )
        return self

    def on_trace_update_do_nothing(self) -> "Arrangements":
        self.fixtures.trace.update.return_value = None
        return self


class Assertions:

    def __init__(self, arrangements: Arrangements):
        self.fixtures = arrangements.fixtures
        self.arrangements = arrangements

    def assert_scores_uploaded(self, number_of_items: int) -> "Assertions":
        number_of_not_nan = len(
            [
                value
                for value in self.fixtures.scores.values()
                if not np.isnan(value)
            ]
        )
        assert (
            self.fixtures.trace.score.call_count
            == number_of_items * number_of_not_nan
        )
        return self

    def assert_chat_called_correctly(
        self, number_of_items: int
    ) -> "Assertions":
        if number_of_items <= 0:
            return self

        self.arrangements.chat_engine.chat.assert_called_with(
            message="query",
            chat_history=[],
            chainlit_message_id=None,
            source_process=SourceProcess.DEPLOYMENT_EVALUATION,
        )
        return self


class Manager:

    def __init__(self, arrangements: Arrangements):
        self.fixtures = arrangements.fixtures
        self.arrangements = arrangements
        self.assertions = Assertions(arrangements)

    def get_service(self) -> LangfuseEvaluator:
        return self.arrangements.service


class TestLangfuseEvaluator:

    @pytest.mark.parametrize(
        "number_of_items,scores",
        [
            (
                1,
                {
                    "answer_relevancy": 0.0,
                    "context_recall": 0.0,
                    "faithfulness": np.nan,
                    "harmfulness": np.nan,
                },
            ),
            (
                3,
                {
                    "answer_relevancy": 0.0,
                    "context_recall": 0.0,
                    "faithfulness": np.nan,
                    "harmfulness": np.nan,
                },
            ),
            (
                1,
                {
                    "answer_relevancy": np.nan,
                    "context_recall": np.nan,
                    "faithfulness": np.nan,
                    "harmfulness": np.nan,
                },
            ),
            (
                5,
                {
                    "answer_relevancy": np.nan,
                    "context_recall": np.nan,
                    "faithfulness": np.nan,
                    "harmfulness": np.nan,
                },
            ),
        ],
    )
    def test_given_response_and_item_when_evaluate_return_results(
        self, number_of_items: int, scores: dict
    ) -> None:
        # Arrange
        manager = Manager(
            Arrangements(
                Fixtures()
                .with_items(number_of_items)
                .with_dataset()
                .with_response()
                .with_trace()
                .with_scores(scores)
            )
            .on_langfuse_dataset_service_get_dataset_return_dataset()
            .on_chat_engine_chat_return_response()
            .on_ragas_evaluator_evaluate_return_scores()
            .on_chat_engine_get_current_langfuse_trace_return_trace()
        )
        service = manager.get_service()

        # Act
        service.evaluate(manager.fixtures.dataset_name)

        # Assert
        manager.assertions.assert_scores_uploaded(
            number_of_items
        ).assert_chat_called_correctly(number_of_items)
