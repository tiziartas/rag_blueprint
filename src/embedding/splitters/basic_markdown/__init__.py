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
    """
    Register the Basic Markdown splitter components in the application registries.

    This function performs two registrations:
    1. Registers the BasicMarkdownSplitterFactory in the SplitterRegistry
    2. Registers the BasicMarkdownSplitterConfiguration in the SplitterConfigurationRegistry

    Both registrations use the SplitterName.BASIC_MARKDOWN identifier to associate
    the factory and configuration with the Basic Markdown splitter functionality.

    These registrations make the Basic Markdown splitter available for use in the
    document splitting pipeline.
    """
    SplitterRegistry.register(
        SplitterName.BASIC_MARKDOWN, BasicMarkdownSplitterFactory
    )
    SplitterConfigurationRegistry.register(
        SplitterName.BASIC_MARKDOWN, BasicMarkdownSplitterConfiguration
    )
