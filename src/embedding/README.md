# Embedding Module

This module handles document embedding operations for the RAG system, converting text content into vector representations and storing them in vector databases.

## Supported Vector Stores

[Qdrant](https://qdrant.tech/) • [Chroma](https://www.trychroma.com/) • [PGVector](https://github.com/pgvector)

For adding a new vector store support check [How to Add a New Vector Store Implementation](https://feld-m.github.io/rag_blueprint/how_to/how_to_add_new_vector_store//) guide.

## Supported Embedding Models

[VoyageAI](https://www.voyageai.com/) • [OpenAI](https://openai.com/) • [Hugging Face](https://huggingface.co/)

For adding a new embedding model support check [How to Add a New Embedding Model Implementation](https://feld-m.github.io/rag_blueprint/how_to/how_to_add_new_embedding_model/) guide.

## Architecture

<div align="center">
  <img src="/res/readme/Embedding.png" width="600">
  <p><em>Figure 1: High-level architecture embedding process.</em></p>
</div>

### Core Components

- **Vector Store**: Defines vector store used for nodes embeddings
- **Splitter**: Segments content into appropriate chunks
- **Embedding Model**: Defines model used for embeddings
- **Embedder**: Implements nodes embedding and saving them to vector store
- **Orchestrator**: Coordinates embedding process

### Plugin Design

Each datasource is a self-contained implementation within a single directory e.g. `embedding_models`. It serves as a preparation for a future plugin design architecture, to include only the datasources that are necessary.
