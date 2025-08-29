import sys
import pytest
import asyncio
from unittest.mock import MagicMock, patch

sys.path.append("./src")

from extraction.datasources.hackernews.reader import (
    HackerNewsDatasourceReader,
    HackerNewsDatasourceReaderFactory,
)


@pytest.fixture
def mock_configuration():
    mock_conf = MagicMock()
    mock_conf.export_limit = 2
    return mock_conf


@pytest.fixture
def mock_client():
    return MagicMock()


@pytest.mark.asyncio
async def test_reader_initialization(mock_configuration, mock_client):
    reader = HackerNewsDatasourceReader(configuration=mock_configuration, client=mock_client)

    assert reader.export_limit == mock_configuration.export_limit
    assert reader.client == mock_client
    assert hasattr(reader, "logger")


@pytest.mark.asyncio
async def test_read_all_async_yields_stories(mock_configuration, mock_client, caplog):
    # Fake stories returned by the client
    mock_client.get_top_stories_with_details.return_value = [
        {"id": 1, "title": "Story 1"},
        {"id": 2, "title": "Story 2"},
    ]

    reader = HackerNewsDatasourceReader(configuration=mock_configuration, client=mock_client)

    results = []
    async for story in reader.read_all_async():
        results.append(story)

    assert results == [
        {"id": 1, "title": "Story 1"},
        {"id": 2, "title": "Story 2"},
    ]
    assert "Reading stories from Hacker News" in caplog.text
    assert "Fetched Hacker News story" in caplog.text


@pytest.mark.asyncio
async def test_read_all_async_respects_export_limit(mock_configuration, mock_client):
    mock_configuration.export_limit = 1
    mock_client.get_top_stories_with_details.return_value = [
        {"id": 1, "title": "Story 1"},
        {"id": 2, "title": "Story 2"},
    ]

    reader = HackerNewsDatasourceReader(configuration=mock_configuration, client=mock_client)

    results = []
    async for story in reader.read_all_async():
        results.append(story)

    # Should only yield 1 because of export_limit
    assert results == [{"id": 1, "title": "Story 1"}]


def test_factory_creates_reader(mock_configuration):
    with patch(
        "extraction.datasources.hackernews.reader.HackerNewsClientFactory"
    ) as mock_factory:
        fake_client = MagicMock()
        mock_factory.create.return_value = fake_client

        reader = HackerNewsDatasourceReaderFactory._create_instance(mock_configuration)

        assert isinstance(reader, HackerNewsDatasourceReader)
        assert reader.client == fake_client
        mock_factory.create.assert_called_once_with(mock_configuration)

