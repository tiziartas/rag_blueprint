# RAG Blueprint Documentation

## Overview
The RAG blueprint project is a Retrieval-Augmented Generation system that integrates with several datasources to provide intelligent document search and analysis. The system combines the power of different large language models with knowledge bases to deliver accurate, context-aware responses through a chat interface. Codebase provides out-of-the-box integration with UI and observability services.

## Data Sources

| Data Source | Description |
|-------------|-------------|
| [Confluence](https://www.atlassian.com/software/confluence?gclsrc=aw.ds&&campaign=19280571316&adgroup=144874483655&targetid=kwd-22737151&matchtype=e&network=g&device=c&device_model=&creative=665271020076&keyword=confluence&placement=&target=&ds_eid=700000001542923&ds_e1=GOOGLE&gad_source=1&gclid=CjwKCAjwp8--BhBREiwAj7og1-IRQKLqpRA6GsxWCxP79pA8N6llomLslpQ-rTMkvMwKIIdA1Zq3uBoCpjYQAvD_BwE) | Enterprise wiki and knowledge base integration |
| [Notion](https://www.notion.com/) | Workspace and document management integration |
| PDF | PDF document processing and text extraction |
| Bundestag | Data source fetching speeches from [BundestagMine](https://bundestag-mine.de/api/documentation/index.html) |

Check how to configure datasources [here](how_to/how_to_configure/#datasource-configuration).

## Embeddding Models

| Models | Provider | Description |
|-------|----------|-------------|
|   *   | [HuggingFace](https://huggingface.co/) | Open-sourced, run locally embedding models provided by HuggingFace |
|   *   | [OpenAI](https://openai.com/) | Embedding models provided by OpenAI |
|   *   | [VoyageAI](https://www.voyageai.com/) | Embedding models provided by VoyageAI |

Check how to configure embedding model [here](how_to/how_to_configure/#embedding-model-configuration).

## Language Models

| Model | Provider | Description |
|-------|----------|-------------|
|   *   | [LiteLLM](https://docs.litellm.ai/) | Availability of many LLMs via providers like **OpenAI**, **Google** or **Anthropic** as well as local LLMs |


Check how to configure LLM [here](how_to/how_to_configure/#llm-configuration).

## Vector Databases

| Vector Store | Description |
|--------------|-------------|
| [Qdrant](https://qdrant.tech/) | High-performance vector similarity search engine |
| [Chroma](https://www.trychroma.com/) |  Lightweight embedded vector database |
| [PGVector](https://github.com/pgvector) | Postgres extension for embedding data support |


Check how to configure vector store [here](how_to/how_to_configure/#vector-store-configuration).

## Key Features

- **Multiple Knowledge Base Integration**: Seamless extraction from several Data Sources (Confluence, Notion, PDF)
- **Wide Models Support**: Availability of numerous embedding and language models
- **Vector Search**: Efficient similarity search using vector stores
- **Interactive Chat**: User-friendly interface for querying knowledge on [Chainlit](https://chainlit.io/)
- **Performance Monitoring**: Query and response tracking with [Langfuse](https://langfuse.com/)
- **Evaluation**: Comprehensive evaluation metrics using [RAGAS](https://docs.ragas.io/en/stable/)
- **Setup flexibility**: Easy and flexible setup process of the pipeline

### Quick Start
- [QuickStart Setup](quickstart/quickstart_setup.md)
- [Dveloper Setup](quickstart/developer_setup.md)
