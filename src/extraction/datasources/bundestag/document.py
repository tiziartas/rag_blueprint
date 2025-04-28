from typing import List

from extraction.datasources.core.document import BaseDocument


class BundestagMineDocument(BaseDocument):
    """
    Represents a document from the Bundestag datasource.
    Inherits from BaseDocument and includes additional metadata specific to Bundestag documents.
    """

    included_embed_metadata_keys: List[str] = [
        "title",
        "created_time",
        "last_edited_time",
        "speaker_party",
        "speaker",
    ]

    included_llm_metadata_keys: List[str] = [
        "title",
        "created_time",
        "last_edited_time",
        "speaker_party",
        "speaker",
    ]
