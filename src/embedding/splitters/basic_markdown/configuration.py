from pydantic import Field

from embedding.bootstrap.configuration.splitting_configuration import (
    SplitterConfiguration,
    SplitterName,
)


class BasicMarkdownSplitterConfiguration(SplitterConfiguration):
    """
    Configuration for the BasicMarkdownSplitter. This class defines the parameters needed to split markdown documents into chunks
    with specific token sizes and overlaps.
    """

    chunk_overlap_in_tokens: int = Field(
        ..., description="The number of tokens that overlap between chunks."
    )
    chunk_size_in_tokens: int = Field(
        ..., description="The size of each chunk in tokens."
    )
    name: SplitterName = Field(
        SplitterName.BASIC_MARKDOWN, description="The name of the splitter."
    )
