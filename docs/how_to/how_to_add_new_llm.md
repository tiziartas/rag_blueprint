# How to Add a New LLM Implementation

This guide demonstrates how to add support for a new Language Model (LLM) implementation, using OpenAI as an example.

## Architecture

Large Language Models are mainly responsible for generating the answers based on the user query and retrieved nodes, injected as a context. They are also used in the evaluation process. Additionally, they can be used in various components e.g. `AutoRetriever`.

# Implementation


## Step 1: Dependencies

Add the required packages to `pyproject.toml`:

```toml
[project.optional-dependencies]
augmentation = [
    "llama-index-llms-openai>=0.3.25",
    ...
]
```

## Step 2: LLM Enum

LLM configuration is scoped by provider. Each provider, such as [OpenAI](https://openai.com/), requires its own Pydantic configuration class. Begin by assigning a meaningful name to the new provider in the `LLMProviderName` enumeration in [llm_configuration.py](https://github.com/feld-m/rag_blueprint/blob/main/src/augmentation/bootstrap/configuration/components/llm_configuration.py):

```py
class LLMProviderName(str, Enum):
    ...
    OPENAI = "openai"
```

## Step 3: LLM Configuration And Secrets

Create a new directory `src/augmentation/components/llms/openai` and create a `configuration.py` file in it. This configuration file will contain necessary fields and secrets for setup.


```py
from typing import Literal
from pydantic import ConfigDict, Field, SecretStr
from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMConfiguration,
    LLMProviderName,
)
from core.base_configuration import BaseSecrets


class OpenAILLMConfiguration(LLMConfiguration):
    class Secrets(BaseSecrets):
        model_config = ConfigDict(
            env_file_encoding="utf-8",
            env_prefix="RAG__LLMS__OPENAI__",
            env_nested_delimiter="__",
            extra="ignore",
        )

        api_key: SecretStr = Field(
            ..., description="API key for the model provider."
        )

    provider: Literal[LLMProviderName.OPENAI] = Field(
        ..., description="The name of the language model provider."
    )
    secrets: Secrets = Field(
        None, description="The secrets for the language model."
    )
```

The first part is to create a configuration that extends `LLMConfiguration`. `provider` field constraints the value to `LLMProviderName.OPENAI`, which serves as an indicator for pydantic validator. The `Secrets` inner class defines secret fields that will be present in the environment secret file under the `RAG__LLMS__OPENAI__` prefix. Add the corresponding environment variables to `configurations/secrets.{environment}.env`:

```sh
RAG__LLMS__OPENAI__API_KEY=<openai_api_key>
```

## Step 4: LLM Implementation

In the `llm.py` file, create singleton LLM factory. It provides a framework, where LLM can be retrieved through `OpenaAILLMFactory` and is initialized only once per runtime, saving up the memory (e.g. in cases of small in-memory LLMs). To do so, define expected `_configuration_class` type and provide `_create_instance` implementation using `llamaindex`.


```py
from typing import Type
from llama_index.llms.openai import OpenAI
from augmentation.components.llms.openai.configuration import (
    OpenAILLMConfiguration,
)
from core import SingletonFactory


class OpenaAILLMFactory(SingletonFactory):
    _configuration_class: Type = OpenAILLMConfiguration

    @classmethod
    def _create_instance(cls, configuration: OpenAILLMConfiguration) -> OpenAI:
        return OpenAI(
            api_key=configuration.secrets.api_key.get_secret_value(),
            model=configuration.name,
            max_tokens=configuration.max_tokens,
            max_retries=configuration.max_retries,
        )
```

## Step 5: LLM Output Extractor

Human feedback feature between Chainlit and Langfuse require extraction of information about LLM response. Each provider returns the differently structured output dictionary. Therefore, we need to implement an extractor of required fields. Create `output_extractor.py`:

```py
from typing import Type
from langfuse.api.resources.commons.types.trace_with_details import (
    TraceWithDetails,
)
from augmentation.components.llms.core.base_output_extractor import (
    BaseLlamaindexLLMOutputExtractor,
)
from augmentation.components.llms.openai.configuration import (
    OpenAILLMConfiguration,
)
from core.base_factory import Factory


class OpenAILlamaindexLLMOutputExtractor(BaseLlamaindexLLMOutputExtractor):

    def get_text(self, trace: TraceWithDetails) -> str:
        return trace.output["blocks"][0]["text"]

    def get_generated_by_model(self, trace: TraceWithDetails) -> str:
        return self.configuration.name
```

Implemented interface `BaseLlamaindexLLMOutputExtractor`, provide sufficient extractor for `ChainlitFeedbackService` purposes. Now just add correspodning factory:

```py
class OpenAILlamaindexLLMOutputExtractorFactory(Factory):
    _configuration_class: Type = OpenAILLMConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: OpenAILLMConfiguration
    ) -> OpenAILlamaindexLLMOutputExtractor:
        return OpenAILlamaindexLLMOutputExtractor(configuration)
```

## Step 6: LLM Integration

Create an `__init__.py` file as follows:

```py
from augmentation.bootstrap.configuration.components.llm_configuration import (
    LLMConfigurationRegistry,
    LLMProviderName,
)
from augmentation.components.llms.openai.configuration import (
    OpenAILLMConfiguration,
)
from augmentation.components.llms.openai.llm import OpenaAILLMFactory
from augmentation.components.llms.openai.output_extractor import (
    OpenAILlamaindexLLMOutputExtractorFactory,
)
from augmentation.components.llms.registry import (
    LlamaindexLLMOutputExtractorRegistry,
    LLMRegistry,
)


def register() -> None:
    LLMRegistry.register(LLMProviderName.OPENAI, OpenaAILLMFactory)
    LLMConfigurationRegistry.register(
        LLMProviderName.OPENAI, OpenAILLMConfiguration
    )
    LlamaindexLLMOutputExtractorRegistry.register(
        LLMProviderName.OPENAI, OpenAILlamaindexLLMOutputExtractorFactory
    )
```

The initialization file includes a `register()` method responsible for registering our configuration, output extractor and LLM factories. Registries are used to dynamically inform the system about available implementations. This way, with the following OpenAI configuration in `configurations/configuration.{environment}.json` file:

```json
"augmentation":
{
    "synthesizer":
    {
        "llm": {
            "provider": "openai",
            "name": "gpt-4o",     // any model name compatible with OpenAI API

        }
    }
    ...
}
```

**_Note_**: You can use any `name` exposed by OpenAI

We can dynamically retrieve the corresponding LLM implementation by using the name specified in the configuration:

```py
llm_config = read_llm_from_config()
llm_model = LLMRegistry.get(llm_config.name).create(llm_config)
```

This mechanism is later used by the query engine to initialize the llm defined in the configuration. These steps conclude the implementation, resulting in the following file structure:

```
src/
└── augmentation/
    └── components/
        └── llms/
            └── openai/
                ├── __init__.py
                ├── configuration.py
                ├── llm.py
                └── output_extractor.py
```
