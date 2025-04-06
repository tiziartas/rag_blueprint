# Extraction Module

This module handles data extraction from various sources and transforms content into a standardized markdown format for the RAG system.

## Supported Data Sources

[Notion](https://developers.notion.com/) • [Confluence](https://developer.atlassian.com/cloud/confluence/rest/v2/intro/#about) • PDF files

 **Extending**

For adding a new datasource support check [How to Add a New Datasource Implementation](https://feld-m.github.io/rag_blueprint/how_to/how_to_add_new_datasource/) guide.

## Architecture

<div align="center">
  <img src="/res/readme/Extraction.png" width="600">
  <p><em>Figure 1: High-level architecture extraction process.</em></p>
</div>

### Core Components

- **Orchestrator**: Coordinates extraction from multiple datasources
- **Manager**: Handles the extraction pipeline for each datasource
- **Reader**: Extracts raw content from the source
- **Parser**: Converts raw content to markdown format
- **Cleaner**: Sanitizes and normalizes content
- **Splitter**: Segments content into appropriate chunks

```
extraction/
├── bootstrap/          # Initialization and configuration
├── datasources/        # Source-specific implementations
│   ├── confluence/     # Confluence integration
│   ├── notion/         # Notion integration
│   ├── pdf/            # PDF file processing
│   └── core/           # Base classes and interfaces
└── orchestrators/      # Orchestration implementations
```

### Package Implementation

Currently extraction is implemented as a package that is directly used by Embedding Service. It is planned to decouple it as a separate service in the futre.

### Plugin Design

Each datasource is a self-contained implementation within a single directory e.g. `confluence`. It serves as a preparation for a future plugin design architecture, to include only the datasources that are necessary.
