from extraction.datasources.core.document import BaseDocument


class NotionDocument(BaseDocument):
    """Document representation for Notion page content.

    Extends BaseDocument to handle Notion-specific document processing including
    metadata handling and filtering for embeddings and LLM contexts.

    Attributes:
        attachments: Dictionary of document attachments
        text: Document content in markdown format
        metadata: Extracted page metadata including dates and source info
        excluded_embed_metadata_keys: Metadata keys to exclude from embeddings
        excluded_llm_metadata_keys: Metadata keys to exclude from LLM context
    """

    pass
