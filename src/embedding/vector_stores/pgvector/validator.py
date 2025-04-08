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
    vector store backend. This validator ensures we don't create duplicate tables
    in the database.
    """

    def __init__(
        self,
        configuration: PGVectorStoreConfiguration,
        client: PGVectorClient,
    ):
        """Initialize the PGVector validator with configuration and client.

        Args:
            configuration: Configuration for the PGVector store
            client: PostgreSQL connection client
        """
        self.configuration = configuration
        self.client = client

    def validate(self) -> None:
        """Validate the PGVector configuration settings.

        Runs all validation checks to ensure the vector store can be properly initialized.

        Raises:
            CollectionExistsException: If the collection already exists in database
        """
        self.validate_collection()

    def validate_collection(self) -> None:
        """Validate that the PGVector collection (table) doesn't already exist.

        Checks if a table with the same name exists in the PostgreSQL database
        to prevent duplicate collections.

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
    """Factory for creating configured PGVector store validators.

    Creates and manages singleton instances of validators for PostgreSQL
    vector store backends.

    Attributes:
        _configuration_class: Type of the configuration class used for validation.
    """

    _configuration_class: Type = PGVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: PGVectorStoreConfiguration
    ) -> PGVectorStoreValidator:
        """Creates a PGVector validator based on provided configuration.

        Args:
            configuration: PostgreSQL vector store connection configuration.

        Returns:
            PGVectorStoreValidator: Configured validator instance.
        """
        client = PGVectorStoreClientFactory.create(configuration)
        return PGVectorStoreValidator(
            configuration=configuration, client=client
        )
