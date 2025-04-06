from typing import List

from extraction.datasources.core.document import BaseDocument


class PDFDocument(BaseDocument):
    """Document representation for PDF file content.

    Extends BaseDocument to handle PDF-specific document processing including
    metadata filtering for embeddings and LLM contexts.

    Attributes:
        included_embed_metadata_keys: Metadata keys to include in embeddings
        included_llm_metadata_keys: Metadata keys to include in LLM context
    """

    included_embed_metadata_keys: List[str] = [
        "Title",
        "CreationDate",
        "ModDate",
        "creation_date",
        "client_name",
        "offer_name",
        "project_lead",
    ]
    included_llm_metadata_keys: List[str] = [
        "Title",
        "CreationDate",
        "ModDate",
        "creation_date",
        "client_name",
        "offer_name",
        "project_lead",
    ]
