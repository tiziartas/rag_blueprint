# Augmentation Module

This module implements Retrieval-Augmented Generation (RAG) functionality, combining document retrieval with language model generation to produce accurate, context-aware responses. It integrates Chainlit UI and Langfuse observability with the rest of the system.

## Supported Large Language Models

[OpenAI](https://openai.com/) • Any [OpenAI](https://openai.com/) API compatible models

For adding a new LLM support check [How to Add a New LLM Implementation](https://feld-m.github.io/rag_blueprint/how_to/how_to_add_new_llm/) guide.


## Supported User Interface and Observability Services

[Chainlit](https://chainlit.io/) • [Langfuse](https://langfuse.com/)

## Architecture

<div align="center">
  <img src="/res/readme/Augmentation.png" width="800">
  <p><em>Figure 1: High-level architecture augmentation process.</em></p>
</div>


### Core Components

- **LLMs**: Language model integrations for response generation
- **Retrievers**: Fetch relevant documents
- **Postprocessors**: Refine retrieved documents
- **Chat Engines**: Coordinate context retrieval and answer generation


### Supporting Components

- **Chainlit**: Chat interface and feedback collection
- **Langfuse**: Observability, tracing and evaluation datasets management

### Plugin Design

Each datasource is a self-contained implementation within a single directory e.g. `llms`. It serves as a preparation for a future plugin design architecture, to include only the datasources that are necessary.
