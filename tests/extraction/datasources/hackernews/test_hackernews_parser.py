import sys
import pytest
from unittest.mock import MagicMock

sys.path.append("./src")

from extraction.datasources.hackernews.parser import (
    HackerNewsDatasourceParser,
    HackerNewsDatasourceParserFactory,
)
from extraction.datasources.hackernews.client import StoryItem
from extraction.datasources.hackernews.document import HackerNewsDocument


@pytest.fixture
def story_item():
    """Fixture for a valid StoryItem."""
    return StoryItem(
        id=101,
        title="A sample story",
        url="https://example.com/story",
        score=99,
        by="bob",
        time=1700000000,
    )


def test_extract_metadata(story_item):
    parser = HackerNewsDatasourceParser()

    metadata = parser._extract_metadata(story_item)

    assert metadata == {
        "id": 101,
        "title": "A sample story",
        "url": "https://example.com/story",
        "score": 99,
        "by": "bob",
        "time": 1700000000,
    }


def test_parse_returns_hackernews_document(story_item):
    parser = HackerNewsDatasourceParser()

    document = parser.parse(story_item)

    assert isinstance(document, HackerNewsDocument)
    assert document.text == "A sample story"
    assert document.metadata["id"] == 101
    assert document.metadata["score"] == 99
    assert document.metadata["by"] == "bob"


def test_factory_creates_parser_instance():
    mock_conf = MagicMock()

    parser = HackerNewsDatasourceParserFactory._create_instance(mock_conf)

    assert isinstance(parser, HackerNewsDatasourceParser)

