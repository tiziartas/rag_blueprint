from typing import Type

from chromadb import HttpClient as ChromaHttpClient
from chromadb.api import ClientAPI as ChromaClient

from core.base_factory import SingletonFactory
from embedding.vector_stores.chroma.configuration import (
    ChromaVectorStoreConfiguration,
)


class ChromaVectorStoreClientFactory(SingletonFactory):
    _configuration_class: Type = ChromaVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: ChromaVectorStoreConfiguration
    ) -> ChromaClient:
        return ChromaHttpClient(
            host=configuration.host,
            port=configuration.ports.rest,
        )
