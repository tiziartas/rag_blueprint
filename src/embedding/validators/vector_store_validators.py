from abc import ABC, abstractmethod

from chromadb.api import ClientAPI as ChromaClient
from psycopg2.extensions import connection as PGVectorClient
from qdrant_client import QdrantClient

from common.bootstrap.configuration.pipeline.embedding.vector_store.vector_store_configuration import (
    ChromaConfiguration,
    PGVectorConfiguration,
    QDrantConfiguration,
)
from common.exceptions import CollectionExistsException


class VectorStoreValidator(ABC):

    @abstractmethod
    def validate(self) -> None:
        """
        Validate the vector store settings.
        """
        pass


class QdrantVectorStoreValidator(VectorStoreValidator):
    """Validator for Qdrant vector store configuration.

    Validates collection settings and existence for Qdrant
    vector store backend.

    Attributes:
        configuration: Settings for vector store
        qdrant_client: Client for Qdrant interactions
    """

    def __init__(
        self,
        configuration: QDrantConfiguration,
        qdrant_client: QdrantClient,
    ):
        """Initialize validator with configuration and client.

        Args:
            configuration: Qdrant vector store settings
            qdrant_client: Client for Qdrant operations
        """
        self.configuration = configuration
        self.qdrant_client = qdrant_client

    def validate(self) -> None:
        """
        Valiuate the Qdrant vector store settings.
        """
        self.validate_collection()

    def validate_collection(self) -> None:
        """Validate Qdrant collection existence.

        Raises:
            CollectionExistsException: If collection already exists
        """
        collection_name = self.configuration.collection_name
        if self.qdrant_client.collection_exists(collection_name):
            raise CollectionExistsException(collection_name)


class ChromaVectorStoreValidator(VectorStoreValidator):
    """Validator for Chroma vector store configuration.

    Validates collection settings and existence for Chroma
    vector store backend.

    Attributes:
        configuration: Settings for vector store
        chroma_client: Client for Chroma interactions
    """

    def __init__(
        self,
        configuration: ChromaConfiguration,
        chroma_client: ChromaClient,
    ):
        """Initialize validator with configuration and client.

        Args:
            configuration: Chroma vector store settings
            chroma_client: Client for Chroma operations
        """
        self.configuration = configuration
        self.chroma_client = chroma_client

    def validate(self) -> None:
        """
        Valiuate the Chroma vector store settings.
        """
        self.validate_collection()

    def validate_collection(self) -> None:
        """Validate Chroma collection existence.

        Raises:
            CollectionExistsException: If collection already exists
        """
        collection_name = self.configuration.collection_name
        if collection_name in self.chroma_client.list_collections():
            raise CollectionExistsException(collection_name)


class PGVectorStoreValidator(VectorStoreValidator):
    """Validator for Postgres vector store configuration.

    Validates the existence of a table (treated as a collection) in the Postgres
    vector store backend.

    Attributes:
        configuration: Settings for vector store
        postgres_client: Postgres connection
    """

    def __init__(
        self,
        configuration: PGVectorConfiguration,
        postgres_client: PGVectorClient,
    ):
        self.configuration = configuration
        self.postgres_client = postgres_client

    def validate(self) -> None:
        """
        Validate the PGVector settings.
        """
        self.validate_collection()

    def validate_collection(self) -> None:
        """
        Validate PGVector table existence.

        Raises:
            CollectionExistsException: If the table (collection) already exists.
        """
        collection_name = self.configuration.collection_name
        with self.postgres_client.cursor() as cursor:
            query = f"SELECT to_regclass('data_{collection_name}');"
            cursor.execute(query)
            result = cursor.fetchone()[0]
            if result is not None:
                raise CollectionExistsException(collection_name)
