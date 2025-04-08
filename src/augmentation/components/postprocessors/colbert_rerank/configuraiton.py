from enum import Enum
from typing import Literal

from pydantic import Field

from augmentation.bootstrap.configuration.components.postprocessors_configuration import (
    PostProcessorConfiguration,
    PostProcessorName,
)


class ColbertRerankConfiguration(PostProcessorConfiguration):
    """
    Configuration for the ColBERT reranking postprocessor.

    This class defines the settings needed to perform document reranking
    using the ColBERT retrieval model, which improves search quality through
    late interaction between queries and documents.
    """

    class Models(str, Enum):
        """Supported ColBERT models for reranking."""

        COLBERTV2 = "colbert-ir/colbertv2.0"

    class Tokenizers(str, Enum):
        """Supported tokenizers for ColBERT reranking."""

        COLBERTV2 = "colbert-ir/colbertv2.0"

    name: Literal[PostProcessorName.COLBERT_RERANK] = Field(
        ..., description="The name of the postprocessor."
    )
    model: Models = Field(
        Models.COLBERTV2, description="Model used for reranking"
    )
    tokenizer: Tokenizers = Field(
        Tokenizers.COLBERTV2, description="Tokenizer used for reranking"
    )
    top_n: int = Field(5, description="Number of documents to be reranked")
    keep_retrieval_score: bool = Field(
        True,
        description="Toggle to keep the retrieval score after the reranking",
    )
