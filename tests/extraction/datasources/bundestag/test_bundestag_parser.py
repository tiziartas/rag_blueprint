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

    def with_invalid_response(self) -> "Fixtures":
        self.sample_response = {}  # Empty dictionary missing required fields
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
        sample = self.fixtures.sample_response
        assert metadata["datasource"] == "bundestag"
        assert metadata["language"] == "de"
        assert (
            metadata["url"]
            == f"https://dserver.bundestag.de/btp/{sample['legislaturePeriod']}/{sample['legislaturePeriod']}{sample['protocolNumber']}.pdf"
        )
        assert (
            metadata["title"]
            == f"Protocol/Legislature/AgendaItem {sample['protocolNumber']}/{sample['legislaturePeriod']}/{sample['agendaItemNumber']}"
        )
        assert metadata["format"] == "md"
        assert metadata["created_time"] == sample["date"]
        assert metadata["last_edited_time"] == sample["date"]
        assert metadata["speaker_party"] == sample["speaker"]["party"]
        assert (
            metadata["speaker"]
            == f"{sample['speaker']['firstName']} {sample['speaker']['lastName']}"
        )
        assert metadata["agenda_item_number"] == sample["agendaItemNumber"]
        assert metadata["protocol_number"] == sample["protocolNumber"]
        assert metadata["legislature_period"] == sample["legislaturePeriod"]
        return self

    def assert_none_metadata(self, metadata) -> "Assertions":
        assert metadata is None
        return self

    def assert_document_parsing(
        self, document: BundestagMineDocument
    ) -> "Assertions":
        sample = self.fixtures.sample_response
        assert isinstance(document, BundestagMineDocument)
        assert document.text == sample["text"]
        assert document.metadata["datasource"] == "bundestag"
        assert (
            document.metadata["speaker"]
            == f"{sample['speaker']['firstName']} {sample['speaker']['lastName']}"
        )
        assert (
            document.metadata["title"]
            == f"Protocol/Legislature/AgendaItem {sample['protocolNumber']}/{sample['legislaturePeriod']}/{sample['agendaItemNumber']}"
        )
        return self

    def assert_none_document(self, document) -> "Assertions":
        assert document is None
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

    def test_extract_metadata_with_invalid_input(self):
        """Test the _extract_metadata method with invalid input."""
        # Arrange
        manager = Manager(Arrangements(Fixtures().with_invalid_response()))
        parser = manager.get_parser()

        # Act
        metadata = parser._extract_metadata(manager.fixtures.sample_response)

        # Assert
        manager.assertions.assert_none_metadata(metadata)

    def test_parse_with_invalid_input(self):
        """Test the parse method with invalid input."""
        # Arrange
        manager = Manager(Arrangements(Fixtures().with_invalid_response()))
        parser = manager.get_parser()

        # Act
        document = parser.parse(manager.fixtures.sample_response)

        # Assert
        manager.assertions.assert_none_document(document)
