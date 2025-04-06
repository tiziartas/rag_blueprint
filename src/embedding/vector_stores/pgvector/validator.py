from typing import Type

from psycopg2.extensions import connection as PGVectorClient

from core.base_factory import SingletonFactory
from embedding.vector_stores.core.exceptions import CollectionExistsException
from embedding.vector_stores.core.validator import BaseVectorStoreValidator
from embedding.vector_stores.pgvector.client import PGVectorStoreClientFactory
from embedding.vector_stores.pgvector.configuration import (
    PGVectorStoreConfiguration,
)


class PGVectorStoreValidator(BaseVectorStoreValidator):
    """Validator for Postgres vector store configuration.

    Validates the existence of a table (treated as a collection) in the Postgres
    vector store backend.

    Attributes:
        configuration: Settings for vector store
        client: Postgres connection
    """

    def __init__(
        self,
        configuration: PGVectorStoreConfiguration,
        client: PGVectorClient,
    ):
        self.configuration = configuration
        self.client = client

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
        with self.client.cursor() as cursor:
            query = f"SELECT to_regclass('data_{collection_name}');"
            cursor.execute(query)
            result = cursor.fetchone()[0]
            if result is not None:
                raise CollectionExistsException(collection_name)


class PGVectorStoreValidatorFactory(SingletonFactory):
    """Factory for creating configured Qdrant clients."""

    _configuration_class: Type = PGVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: PGVectorStoreConfiguration
    ) -> PGVectorStoreValidator:
        """Creates a Qdrant client based on provided configuration.

        Args:
            configuration: QDrant connection configuration.

        Returns:
            QdrantClient: Configured client instance.
        """
        client = PGVectorStoreClientFactory.create(configuration)
        return PGVectorStoreValidator(
            configuration=configuration, client=client
        )
