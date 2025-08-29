import sys
import pytest
from unittest.mock import patch, MagicMock
from requests.models import Response

sys.path.append("./src")

from extraction.datasources.hackernews.client import (
    StoryItem,
    HackerNewsClient
)
# -------------------
# Helpers
# -------------------

def make_mock_response(json_data, status_code=200):
    mock_resp = MagicMock(spec=Response)
    mock_resp.json.return_value = json_data
    mock_resp.raise_for_status.side_effect = None if status_code == 200 else Exception("HTTP Error")
    return mock_resp

# -------------------
# Tests
# -------------------
class TestHackerNewsClient:
    @patch.object(HackerNewsClient, "get")
    def test_safe_get_success(self, mock_get):
        client = HackerNewsClient()
        mock_get.return_value = make_mock_response([1, 2, 3])

        result = client.safe_get("topstories.json")

        assert result == [1, 2, 3]
        mock_get.assert_called_once()

    @patch.object(HackerNewsClient, "get")
    def test_safe_get_http_error(self, mock_get):
        client = HackerNewsClient()
        mock_resp = make_mock_response(None, status_code=500)
        mock_resp.raise_for_status.side_effect = Exception("HTTP error")
        mock_get.return_value = mock_resp

        result = client.safe_get("topstories.json")

        assert result is None

    @patch.object(HackerNewsClient, "get")
    def test_safe_get_exception(self, mock_get):
        client = HackerNewsClient()
        mock_get.side_effect = Exception("Network error")

        result = client.safe_get("topstories.json")

        assert result is None

    @patch.object(HackerNewsClient, "safe_get")
    def test_get_top_stories(self, mock_safe_get):
        client = HackerNewsClient()
        mock_safe_get.return_value = list(range(20))

        result = client.get_top_stories()

        assert result == [0, 1, 2, 3, 4]

    @patch.object(HackerNewsClient, "safe_get")
    def test_get_top_stories_none(self, mock_safe_get):
        client = HackerNewsClient()
        mock_safe_get.return_value = None

        result = client.get_top_stories()

        assert result == []

    @patch.object(HackerNewsClient, "safe_get")
    def test_get_item(self, mock_safe_get):
        client = HackerNewsClient()
        mock_safe_get.return_value = {"id": 123, "title": "Test story", "url": "http://x.com", "score": 42, "by": "alice", "time": 1700000000}

        result = client.get_item(123)

        assert result["id"] == 123
        assert result["title"] == "Test story"

    @patch.object(HackerNewsClient, "safe_get")
    def test_get_item_none(self, mock_safe_get):
        client = HackerNewsClient()
        mock_safe_get.return_value = None

        result = client.get_item(123)

        assert result == {}

    @patch.object(HackerNewsClient, "get_item")
    @patch.object(HackerNewsClient, "get_top_stories")
    def test_get_top_stories_with_details(self, mock_get_top_stories, mock_get_item):
        client = HackerNewsClient()
        mock_get_top_stories.return_value = [1]
        mock_get_item.return_value = {"id": 1, "title": "A story", "url": None, "score": 10, "by": "bob", "time": 1700000000}

        stories = list(client.get_top_stories_with_details()

        assert len(stories) == 1
        assert isinstance(stories[0], StoryItem)
        assert stories[0].title == "A story"

    def test_storyitem_validation(self):
        with pytest.raises(ValueError):
            StoryItem(id=1, title=" ", url=None, score=1, by="bob", time=1700000000)
