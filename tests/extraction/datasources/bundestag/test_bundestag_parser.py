import sys

sys.path.append("./src")

from unittest.mock import Mock

from extraction.datasources.bundestag.configuration import (
    BundestagMineDatasourceConfiguration,
)
from extraction.datasources.bundestag.document import BundestagMineDocument
from extraction.datasources.bundestag.parser import (
    BundestagMineDatasourceParser,
)


class Fixtures:
    def __init__(self):
        self.sample_response = None
        self.configuration = None

    def with_sample_response(self) -> "Fixtures":
        self.sample_response = {
            "text": "This is a test markdown content.",
            "legislaturePeriod": "19",
            "protocolNumber": "123",
            "date": "2023-01-01",
            "speaker": {
                "firstName": "John",
                "lastName": "Doe",
                "party": "Test Party",
            },
            "agendaItemNumber": "42",
        }
        return self

    def with_configuration(self) -> "Fixtures":
        self.configuration = Mock(spec=BundestagMineDatasourceConfiguration)
        return self


class Arrangements:
    def __init__(self, fixtures: Fixtures):
        self.fixtures = fixtures
        self.parser = BundestagMineDatasourceParser()


class Assertions:
    def __init__(self, arrangements: Arrangements):
        self.fixtures = arrangements.fixtures
        self.arrangements = arrangements
        self.parser = arrangements.parser

    def assert_metadata_extraction(self, metadata: dict) -> "Assertions":
        assert metadata["datasource"] == "bundestag"
        assert metadata["language"] == "de"
        assert (
            metadata["url"] == "https://dserver.bundestag.de/btp/19/19123.pdf"
        )
        assert metadata["title"] == "Protocol/Legislature 123/19"
        assert metadata["format"] == "md"
        assert metadata["created_time"] == "2023-01-01"
        assert metadata["last_edited_time"] == "2023-01-01"
        assert metadata["speaker_party"] == "Test Party"
        assert metadata["speaker"] == "John Doe"
        assert metadata["agenda_item_number"] == "42"
        assert metadata["protocol_number"] == "123"
        assert metadata["legislature_period"] == "19"
        return self

    def assert_document_parsing(
        self, document: BundestagMineDocument
    ) -> "Assertions":
        assert isinstance(document, BundestagMineDocument)
        assert document.text == "This is a test markdown content."
        assert document.metadata["datasource"] == "bundestag"
        assert document.metadata["speaker"] == "John Doe"
        assert document.metadata["title"] == "Protocol/Legislature 123/19"
        return self


class Manager:
    def __init__(self, arrangements: Arrangements):
        self.fixtures = arrangements.fixtures
        self.arrangements = arrangements
        self.assertions = Assertions(arrangements=arrangements)

    def get_parser(self) -> BundestagMineDatasourceParser:
        return self.arrangements.parser


class TestBundestagMineDatasourceParser:

    def test_extract_metadata(self):
        """Test the _extract_metadata method."""
        # Arrange
        manager = Manager(Arrangements(Fixtures().with_sample_response()))
        parser = manager.get_parser()

        # Act
        metadata = parser._extract_metadata(manager.fixtures.sample_response)

        # Assert
        manager.assertions.assert_metadata_extraction(metadata)

    def test_parse(self):
        """Test the parse method."""
        # Arrange
        manager = Manager(Arrangements(Fixtures().with_sample_response()))
        parser = manager.get_parser()

        # Act
        document = parser.parse(manager.fixtures.sample_response)

        # Assert
        manager.assertions.assert_document_parsing(document)
