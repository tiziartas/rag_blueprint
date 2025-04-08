from typing import Type

from psycopg2 import connect
from psycopg2.extensions import connection as PGVectorClient

from core.base_factory import SingletonFactory
from embedding.vector_stores.pgvector.configuration import (
    PGVectorStoreConfiguration,
)


class PGVectorStoreClientFactory(SingletonFactory):
    """
    Factory class for creating and managing a singleton instance of the PGVector database client.

    This factory ensures that only one connection to the PGVector database is maintained
    throughout the application lifecycle, following the Singleton pattern.
    """

    _configuration_class: Type = PGVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: PGVectorStoreConfiguration
    ) -> PGVectorClient:
        """
        Creates a new connection to the PGVector database using the provided configuration.

        Args:
            configuration: Configuration object containing connection details and credentials
                           for the PGVector database.

        Returns:
            A connection object to the PGVector database that can be used for database operations.
        """
        return connect(
            host=configuration.host,
            port=configuration.port,
            database=configuration.database_name,
            user=configuration.secrets.username.get_secret_value(),
            password=configuration.secrets.password.get_secret_value(),
        )
