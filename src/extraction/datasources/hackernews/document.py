from typing import List

from extraction.datasources.core.document import BaseDocument


class HackerNewsDocument(BaseDocument):
    """Document representation for Hacker News page content.

    Extends BaseDocument to handle Hacker News-specific document processing including
    content extraction, metadata handling, and exclusion configuration.
    """

    included_embed_metadata_keys: List[str] = [
        "id",
        "title",
        "url",
        "score",
        "by",
        "time",
    ]

    included_llm_metadata_keys: List[str] = [
        "id",
        "title",
        "url",
        "score",
        "by",
        "time"
    ]
