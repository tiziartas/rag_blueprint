from extraction.datasources.core.document import BaseDocument


class ConfluenceDocument(BaseDocument):
    """Document representation for Confluence page content.

    Extends BaseDocument to handle Confluence-specific document processing including
    content extraction, metadata handling, and exclusion configuration.

    Attributes:
        text: Markdown-formatted page content
        attachments: Dictionary of page attachments (placeholder for future)
        metadata: Extracted page metadata including dates, IDs, and URLs
        excluded_embed_metadata_keys: Metadata keys to exclude from embeddings
        excluded_llm_metadata_keys: Metadata keys to exclude from LLM context

    Note:
        Handles conversion of HTML content to markdown and manages metadata
        filtering for both embedding and LLM contexts.
    """

    pass
