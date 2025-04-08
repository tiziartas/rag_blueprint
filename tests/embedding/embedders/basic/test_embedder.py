import sys

sys.path.append("./src")

from typing import List
from unittest.mock import MagicMock, Mock

from llama_index.core import StorageContext
from llama_index.core.base.embeddings.base import BaseEmbedding
from llama_index.core.schema import TextNode
from llama_index.core.vector_stores.types import VectorStore

from embedding.bootstrap.configuration.configuration import (
    EmbeddingConfiguration,
)
from embedding.embedders.basic.embedder import BasicEmbedder


class Fixtures:

    def __init__(self):
        self.nodes: List[TextNode] = []
        self.embeddings: List[List[float]] = []
        self.storage_context: StorageContext = None
        self.vector_store_index_init = None

    def with_nodes(self) -> "Fixtures":
        node = Mock(spec=TextNode)
        node.get_content.return_value = "This is a test node"
        node.embedding = None
        self.nodes.append(node)
        return self

    def with_embeddings(self) -> "Fixtures":
        self.embeddings = [[0.1, 0.2, 0.3]]
        return self

    def with_storage_context(self) -> "Fixtures":
        self.storage_context = Mock(spec=StorageContext)
        return self

    def with_mock_vector_store_index_init(self) -> "Fixtures":
        self.vector_store_index_init = Mock()
        return self


class Arrangements:

    def __init__(self, fixtures: Fixtures) -> None:
        self.fixtures = fixtures

        self.embedding_model: BaseEmbedding = Mock(spec=BaseEmbedding)
        self.vector_store: VectorStore = Mock(spec=VectorStore)
        self.configuration = Mock(spec=EmbeddingConfiguration)
        self.configuration.embedding = Mock()
        self.configuration.embedding.embedding_model = Mock()
        self.configuration.embedding.embedding_model.batch_size = 10
        self.service = BasicEmbedder(
            configuration=self.configuration,
            embedding_model=self.embedding_model,
            vector_store=self.vector_store,
        )
        self.vector_store_index_init = None

    def mock_storage_context(self) -> "Arrangements":
        StorageContext.from_defaults = Mock()
        StorageContext.from_defaults.return_value = (
            self.fixtures.storage_context
        )
        return self

    def mock_vector_store_index_init(self) -> "Arrangements":
        self.vector_store_index_init = MagicMock(return_value=None)
        return self

    def on_get_text_embedding_batch_return_embeddings(self):
        self.embedding_model.get_text_embedding_batch.return_value = (
            self.fixtures.embeddings
        )
        return self


class Assertions:

    def __init__(self, arrangements: Arrangements) -> None:
        self.fixtures = arrangements.fixtures
        self.arrangements = arrangements
        self.service = arrangements.service

    def assert_nodes_embedded(self) -> None:
        for node, embedding in zip(
            self.fixtures.nodes, self.fixtures.embeddings
        ):
            assert node.embedding == embedding


class Manager:

    def __init__(self, arrangements: Arrangements):
        self.fixtures = arrangements.fixtures
        self.arrangements = arrangements
        self.assertions = Assertions(arrangements=arrangements)

    def get_service(self) -> BasicEmbedder:
        return self.arrangements.service


class TestEmbedder:

    def test_given_nodes_when_save_then_nodes_are_saved(self) -> None:
        # Arrange
        manager = Manager(
            Arrangements(
                Fixtures()
                .with_nodes()
                .with_storage_context()
                .with_mock_vector_store_index_init(),
            )
            .mock_storage_context()
            .mock_vector_store_index_init(),
        )

        service = manager.get_service()

        # Act
        service.embed(manager.fixtures.nodes)

        # Assert
        manager.assertions.assert_nodes_embedded()
