import sys
import pytest
from unittest.mock import patch, MagicMock

sys.path.append("./src")

from extraction.datasources.hackernews.manager import (
    HackerNewsDatasourceManagerFactory,
)
from extraction.datasources.core.manager import BasicDatasourceManager


def test_create_instance_returns_manager():
    mock_conf = MagicMock()

    with patch(
        "extraction.datasources.hackernews.manager.HackerNewsDatasourceReaderFactory"
    ) as mock_reader_factory, patch(
        "extraction.datasources.hackernews.manager.HackerNewsDatasourceParserFactory"
    ) as mock_parser_factory:
        # Setup fake reader and parser
        fake_reader = MagicMock()
        fake_parser = MagicMock()
        mock_reader_factory.create.return_value = fake_reader
        mock_parser_factory.create.return_value = fake_parser

        manager = HackerNewsDatasourceManagerFactory._create_instance(mock_conf)

        # Ensure correct return type
        assert isinstance(manager, BasicDatasourceManager)

        # Ensure the factories were called with the configuration
        mock_reader_factory.create.assert_called_once_with(mock_conf)
        mock_parser_factory.create.assert_called_once_with(mock_conf)

        # Ensure manager wiring is correct
        assert manager.reader == fake_reader
        assert manager.parser == fake_parser
        assert manager.configuration == mock_conf
