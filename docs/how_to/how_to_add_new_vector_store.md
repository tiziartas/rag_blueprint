# How to Add a New Vector Store Implementation

This guide demonstrates how to add support for a new vector store implementation, using `Chroma` as an example.

## Architecture

Vector store is used for storing and retrieving embeddings of datasource nodes.

# Implementation

## Step 1: Add Dependencies

Add the required packages to `pyproject.toml`:

```toml
[project.optional-dependencies]
embedding = [
    "chromadb>=0.6.3",
    "llama-index-vector-stores-chroma>=0.4.1",
    ...
]
```

## Step 2: Docker Service

Add the vector store service to [docker-compose.yml](https://github.com/feld-m/rag_blueprint/blob/main/build/workstation/docker/docker-compose.yml):

```yml
name: rag
services:
...
  chroma:
    image: chromadb/chroma:0.6.4.dev19
    environment:
      CHROMA_HOST_PORT: ${RAG__VECTOR_STORE__PORT_REST}
    ports:
      - "${RAG__VECTOR_STORE__PORT_REST}:${RAG__VECTOR_STORE__PORT_REST}"
    restart: unless-stopped
    volumes:
      - ./.docker-data/chroma:/chroma/chroma/
...
```

It enables easy vector store initialization using `init.sh` script.

## Step 3: Vector Store Enum

Add the vector store to the `VectorStoreName` enum in `vector_store_configuration.py`:

```py
class VectorStoreName(str, Enum):
    ...
    CHROMA = "chroma"
```

The enum value must match the service name in the Docker configuration.


## Step 4: Vector Store Configuration

Create a new directory `src/embedding/vector_stores/chroma` and create a `configuration.py` file in it. This configuration file will contain necessary fields for setup.

```py
from typing import Literal
from pydantic import Field
from embedding.bootstrap.configuration.vector_store_configuration import (
    VectorStoreConfiguration,
    VectorStoreName,
)

class ChromaVectorStoreConfiguration(VectorStoreConfiguration):
    """Configuration for the ChromaDB vector store."""

    name: Literal[VectorStoreName.CHROMA] = Field(
        ..., description="The name of the vector store."
    )
```

The first part is to create a configuration that extends `VectorStoreConfiguration`. `name` field constraints the value to `VectorStoreName.CHROMA`, which serves as an indicator for pydantic validator.

**_Note_**: For adding potentially needed secrets support follow the same approach as explained in [How to Add a New LLM Implementation](how_to_add_new_llm.md) guide.

## Step 5: Vector Store Implementation

In the `vector_store.py` file, create singleton vector store factory. It provides a framework, where vector store can be retrieved through ChromaVectorStoreFactory and is initialized only once per runtime, saving up the memory. To do so, define expected `_configuration_class` type and provide `_create_instance` implementation using `llamaindex`.

```py
from typing import Type
from llama_index.vector_stores.chroma import ChromaVectorStore
from core.base_factory import SingletonFactory
from embedding.vector_stores.chroma.configuration import (
    ChromaVectorStoreConfiguration,
)


class ChromaVectorStoreFactory(SingletonFactory):
    _configuration_class: Type = ChromaVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: ChromaVectorStoreConfiguration
    ) -> ChromaVectorStore:
        return ChromaVectorStore(
            host=configuration.host,
            port=str(configuration.port),
            collection_name=configuration.collection_name,
        )
```

The field `_configuration_class` defines the required configuration type. The rest involves implementing
the required `_create_instance` method with the corresponding vector store initialization.

## Step 6: Vector Store Client

We will want to validate our vector store before the run, for that we need and HTTP client. To create a Chroma client, we implement `ChromaVectorStoreClientFactory` in `client.py`. It extends `SingletonFactory`,
which provides an interface for initializing a single instance for the duration of the application runtime.

```py
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
            port=configuration.port,
        )
```

The field `_configuration_class` defines the required configuration type. The rest involves implementing
the required `_create_instance` method with the corresponding client initialization.

## Step 7: Vector Store Validator

Now we can implement the validator that will check if defined vector store collection already exists. Nevertheless, it can be extended to validate other apsects as well. Create `validator.py` file and create `ChromaVectorStoreValidator` that implements `BaseVectorStoreValidator` interface:

```py
from typing import Type
from chromadb.api import ClientAPI as ChromaClient
from core.base_factory import SingletonFactory
from embedding.vector_stores.chroma.client import ChromaVectorStoreClientFactory
from embedding.vector_stores.chroma.configuration import (
    ChromaVectorStoreConfiguration,
)
from embedding.vector_stores.core.exceptions import CollectionExistsException
from embedding.vector_stores.core.validator import BaseVectorStoreValidator

class ChromaVectorStoreValidator(BaseVectorStoreValidator):
    def __init__(
        self,
        configuration: ChromaVectorStoreConfiguration,
        client: ChromaClient,
    ):
        self.configuration = configuration
        self.client = client

    def validate(self) -> None:
        self.validate_collection()

    def validate_collection(self) -> None:
        collection_name = self.configuration.collection_name
        if collection_name in self.client.list_collections():
            raise CollectionExistsException(collection_name)
```

Now add the factory that defines validator initialization.

```py
class ChromaVectorStoreValidatorFactory(SingletonFactory):
    _configuration_class: Type = ChromaVectorStoreConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: ChromaVectorStoreConfiguration
    ) -> ChromaVectorStoreValidator:
        client = ChromaVectorStoreClientFactory.create(configuration)
        return ChromaVectorStoreValidator(
            configuration=configuration, client=client
        )
```

You can notice that we use previously implemented `ChromaVectorStoreClientFactory` to get required client instance.


## Step 8: Vector Store Integration

Create an `__init__.py` file as follows:

```py
from embedding.bootstrap.configuration.vector_store_configuration import (
    VectorStoreConfigurationRegistry,
    VectorStoreName,
)
from embedding.vector_stores.chroma.configuration import (
    ChromaVectorStoreConfiguration,
)
from embedding.vector_stores.chroma.validator import (
    ChromaVectorStoreValidatorFactory,
)
from embedding.vector_stores.chroma.vector_store import ChromaVectorStoreFactory
from embedding.vector_stores.registry import (
    VectorStoreRegistry,
    VectorStoreValidatorRegistry,
)

def register() -> None:
    VectorStoreConfigurationRegistry.register(
        VectorStoreName.CHROMA,
        ChromaVectorStoreConfiguration,
    )
    VectorStoreRegistry.register(
        VectorStoreName.CHROMA, ChromaVectorStoreFactory
    )
    VectorStoreValidatorRegistry.register(
        VectorStoreName.CHROMA, ChromaVectorStoreValidatorFactory
    )
```

The initialization file includes a `register()` method responsible for registering our configuration, and validator and vector store factories. Registries are used to dynamically inform the system about available implementations. This way, with the following Chroma configuration in `configurations/configuration.{environment}.json` file:


```json
    "embedding": {
        "vector_store": {
            "name": "chroma",
            "collection_name": "new-collection",
            "host": "chroma",
            "protocol": "http",
            "port": 6000
        }
        ...
    },
```

We can dynamically retrieve the corresponding vector store implementation by using the name specified in the configuration:


```py
vector_store_config = read_vector_store_from_config()
vector_store = VectorStoreRegistry.get(vector_store_config.name).create(vector_store_config)
vector_store_validator = VectorStoreValidatorRegistry.get(vector_store_config.name).create(vector_store_config)
```

This mechanism is later used by the embedding orchestrator to initialize the vector store defined in the configuration. These steps conclude the implementation, resulting in the following file structure:

```
src/
└── embedding/
    └── vector_stores/
        └── chroma/
            ├── __init__.py
            ├── client.py
            ├── configuration.py
            ├── validator.py
            └── vector_store.py
```
