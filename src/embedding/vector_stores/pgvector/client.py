from typing import Type

from psycopg2 import connect
from psycopg2.extensions import connection as PGVectorClient

from core.base_factory import SingletonFactory
from embedding.vector_stores.pgvector.configuration import (
    PGVectorStoreConfiguration,
)


class PGVectorStoreClientFactory(SingletonFactory):
    _configuration_class: Type = PGVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: PGVectorStoreConfiguration
    ) -> PGVectorClient:
        return connect(
            host=configuration.host,
            port=configuration.port,
            database=configuration.database_name,
            user=configuration.secrets.username.get_secret_value(),
            password=configuration.secrets.password.get_secret_value(),
        )
