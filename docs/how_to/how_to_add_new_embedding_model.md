# How to Add a New Embedding Model Implementation

This guide demonstrates how to add support for a new embedding model implementation, using [VoyageAI](https://www.voyageai.com/) provider as an example.

## Architecture

Embedding models are used to generate the user query and datasource embeddings. These embeddings are used for semantic search and retrieval in the RAG pipeline. Therefore, adding support for a new embedding model requires implementing the configuration and [Llamaindex](https://www.llamaindex.ai/) integration.

# Implementation

## Step 1: Dependencies

Add the required packages to `pyproject.toml` under the following section:

```toml
[project.optional-dependencies]
embedding = [
    "llama-index-embeddings-voyageai>=0.3.5",
    ...
]
```

## Step 2: Embedding Model Enum

Embedding model configuration is scoped by provider. Each provider, such as [Voyage](https://www.voyageai.com/), requires its own Pydantic configuration class. Begin by assigning a meaningful name to the new provider in the `LLMProviderName` enumeration in [embedding_model_configuration.py](https://github.com/feld-m/rag_blueprint/blob/main/src/embedding/bootstrap/configuration/embedding_model_configuration.py):

```py
class EmbeddingModelProviderName(str, Enum):
    ...
    VOYAGE = "voyage"
```

## Step 3: Embedding Model Secrets And Configuration

Create a new directory `src/embedding/embedding_models/voyage` and create a `configuration.py` file in it. This configuration file will contain necessary fields and secrets for setup.

```py
from typing import Literal
from pydantic import ConfigDict, Field, SecretStr
from core.base_configuration import BaseSecrets
from embedding.bootstrap.configuration.embedding_model_configuration import (
    EmbeddingModelConfiguration,
    EmbeddingModelProviderName,
)


class VoyageEmbeddingModelConfiguration(EmbeddingModelConfiguration):

    class Secrets(BaseSecrets):
        model_config = ConfigDict(
            env_file_encoding="utf-8",
            env_prefix="RAGKB__EMBEDDING_MODELS__VOYAGE__",
            env_nested_delimiter="__",
            extra="ignore",
        )

        api_key: SecretStr = Field(..., description="API key for the model")

    provider: Literal[EmbeddingModelProviderName.VOYAGE] = Field(
        ..., description="The provider of the embedding model."
    )
    secrets: Secrets = Field(
        None, description="The secrets for the language model."
    )
```

The first part is to create a configuration that extends `EmbeddingModelConfiguration`. `provider` field constraints the value to `EmbeddingModelProviderName.VOYAGE`, which serves as an indicator for pydantic validator. The `Secrets` inner class defines secret fields that will be present in the environment secret file under the `RAGKB__EMBEDDING_MODELS__VOYAGE__` prefix. Add the corresponding environment variables to `configurations/secrets.{environment}.env`:

```sh
RAGKB__EMBEDDING_MODELS__VOYAGE__API_KEY=<voyage_api_key>
```

> **Note**: If your embedding model doesn't require secrets, you can skip this step.

## Step 4: Embedding Model Implementation

In the `embedding_model.py` file, create singleton embedding model factory. It provides a framework, where embedding model can be retrieved through `VoyageEmbeddingModelFactory` and is initialized only once per runtime, saving up the memory (e.g. in cases of small in-memory embedding models). To do so, define expected `_configuration_class` type and provide `_create_instance` implementation using `llamaindex`.

```py
from typing import Callable, Type
from llama_index.embeddings.voyageai import VoyageEmbedding
from transformers import AutoTokenizer
from core import SingletonFactory
from embedding.embedding_models.voyage.configuration import (
    VoyageEmbeddingModelConfiguration,
)


class VoyageEmbeddingModelFactory(SingletonFactory):
    _configuration_class: Type = VoyageEmbeddingModelConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: VoyageEmbeddingModelConfiguration
    ) -> VoyageEmbedding:
        return VoyageEmbedding(
            voyage_api_key=configuration.secrets.api_key.get_secret_value(),
            model_name=configuration.name,
            embed_batch_size=configuration.batch_size,
        )
```

In the same file implement a factory that defines the tokenizer used along with this embedding model. For the same reasons as previously we use singleton factory.

```py
class VoyageEmbeddingModelTokenizerFactory(SingletonFactory):
    _configuration_class: Type = VoyageEmbeddingModelConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: VoyageEmbeddingModelConfiguration
    ) -> Callable:
        return AutoTokenizer.from_pretrained(
            configuration.tokenizer_name
        ).tokenize
```

## Step 7: Embedding Model Integration

Create an `__init__.py` file as follows:

```py
from embedding.bootstrap.configuration.embedding_model_configuration import (
    EmbeddingModelConfigurationRegistry,
    EmbeddingModelProviderName,
)
from embedding.embedding_models.registry import (
    EmbeddingModelRegistry,
    EmbeddingModelTokenizerRegistry,
)
from embedding.embedding_models.voyage.configuration import (
    VoyageEmbeddingModelConfiguration,
)
from embedding.embedding_models.voyage.embedding_model import (
    VoyageEmbeddingModelFactory,
    VoyageEmbeddingModelTokenizerFactory,
)

def register():
    EmbeddingModelConfigurationRegistry.register(
        EmbeddingModelProviderName.VOYAGE, VoyageEmbeddingModelConfiguration
    )
    EmbeddingModelRegistry.register(
        EmbeddingModelProviderName.VOYAGE, VoyageEmbeddingModelFactory
    )
    EmbeddingModelTokenizerRegistry.register(
        EmbeddingModelProviderName.VOYAGE, VoyageEmbeddingModelTokenizerFactory
    )
```

The initialization file includes a `register()` method responsible for registering our configuration, embedding model and its tokenizer factories. Registries are used to dynamically inform the system about available implementations. This way, with the following Voyage configuration in `configurations/configuration.{environment}.json` file:

```json
    "embedding": {
        "embedding_model": {
            "provider": "voyage",
            "name": "voyage-3", // any model name compatible with VoyageAI API
            "tokenizer_name": "voyageai/voyage-3", // any tokenizer name compatible with VoyageAI and AutoTokenizer
            "splitter": {
                "chunk_overlap_in_tokens": 50,
                "chunk_size_in_tokens": 384
            }
        }
        ...
    }
    ...
```

**_Note_**: You can use any `model_name` and `tokenizer_name` exposed by VoyageAI

We can dynamically retrieve the corresponding embedding model implementation by using the name specified in the configuration:

```py
embedding_model_config = read_embedding_model_from_config()
embedding_model = EmbeddingModelRegistry.get(embedding_model_config.name).create(embedding_model_config)
```

This mechanism is later used by the embedding manager to initialize the embedding model defined in the configuration. These steps conclude the implementation, resulting in the following file structure:

```
src/
└── embedding/
    └── embedding_models/
        └── voyage/
            ├── __init__.py
            ├── configuration.py
            └── embedding_model.py
```
