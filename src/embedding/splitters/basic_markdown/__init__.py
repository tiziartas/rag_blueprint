from embedding.bootstrap.configuration.splitting_configuration import (
    SplitterConfigurationRegistry,
    SplitterName,
)
from embedding.splitters.basic_markdown.basic_markdown_splitter import (
    BasicMarkdownSplitterFactory,
)
from embedding.splitters.basic_markdown.configuration import (
    BasicMarkdownSplitterConfiguration,
)
from embedding.splitters.registry import SplitterRegistry


def register() -> None:
    SplitterRegistry.register(
        SplitterName.BASIC_MARKDOWN, BasicMarkdownSplitterFactory
    )
    SplitterConfigurationRegistry.register(
        SplitterName.BASIC_MARKDOWN, BasicMarkdownSplitterConfiguration
    )
