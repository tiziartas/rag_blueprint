import sys
from unittest.mock import Mock, patch

sys.path.append("./src")

from markitdown import MarkItDown

from extraction.datasources.confluence.configuration import (
    ConfluenceDatasourceConfiguration,
)
from extraction.datasources.confluence.document import ConfluenceDocument
from extraction.datasources.confluence.parser import ConfluenceDatasourceParser
from extraction.datasources.confluence.reader import ConfluencePage


class Fixtures:
    def __init__(self):
        self.page = None
        self.base_url = None
        self.configuration = None
        self.html_content = None
        self.markdown_content = None
        self.space_name = "TEST"

    def with_confluence_page(self) -> "Fixtures":
        self.page = Mock(spec=ConfluencePage)
        self.page.id = "123456"
        self.page.title = "Test Page"
        self.page.history = Mock()
        self.page.history.createdDate = "2023-01-01T00:00:00.000Z"
        self.page.history.lastUpdated = Mock()
        self.page.history.lastUpdated.when = "2023-01-02T00:00:00.000Z"
        self.page.expandable = {"space": f"/space/{self.space_name}"}
        self.page.links = Mock()
        self.page.links.webui = f"/wiki/spaces/{self.space_name}/pages/123456"
        self.page.body = Mock()
        self.page.body.view = Mock()
        self.html_content = (
            "<div><h1>Test Page</h1><p>This is a test page</p></div>"
        )
        self.page.body.view.value = self.html_content
        return self

    def with_empty_content_page(self) -> "Fixtures":
        self.with_confluence_page()
        self.page.body.view.value = ""
        return self

    def with_base_url(self) -> "Fixtures":
        self.base_url = "https://confluence.example.com"
        return self

    def with_configuration(self) -> "Fixtures":
        self.configuration = Mock(spec=ConfluenceDatasourceConfiguration)
        self.configuration.base_url = self.base_url
        return self

    def with_markdown_content(self) -> "Fixtures":
        self.markdown_content = "# Test Page\n\nThis is a test page"
        return self


class Arrangements:
    def __init__(self, fixtures: Fixtures) -> None:
        self.fixtures = fixtures

        self.markdown_parser = Mock(spec=MarkItDown)

        self.service = ConfluenceDatasourceParser(
            configuration=self.fixtures.configuration,
            parser=self.markdown_parser,
        )

    def on_parser_convert_return_markdown(self) -> "Arrangements":
        mock_result = Mock()
        mock_result.text_content = self.fixtures.markdown_content
        self.markdown_parser.convert.return_value = mock_result
        return self

    def mock_tempfile(self) -> "Arrangements":
        self.tempfile_patcher = patch("tempfile.NamedTemporaryFile")
        self.mock_temp_file = self.tempfile_patcher.start()
        mock_file = Mock()
        mock_file.name = "temp_file.html"
        self.mock_temp_file.return_value.__enter__.return_value = mock_file
        return self

    def stop_patches(self):
        if hasattr(self, "tempfile_patcher"):
            self.tempfile_patcher.stop()


class Assertions:
    def __init__(self, arrangements: Arrangements) -> None:
        self.fixtures = arrangements.fixtures
        self.arrangements = arrangements

    def assert_document_text(
        self, document: ConfluenceDocument
    ) -> "Assertions":
        assert document.text == self.fixtures.markdown_content
        return self

    def assert_empty_document_text(
        self, document: ConfluenceDocument
    ) -> "Assertions":
        assert document.text == ""
        return self

    def assert_document_metadata(
        self, document: ConfluenceDocument
    ) -> "Assertions":
        metadata = document.metadata
        self.assert_metadata(metadata)
        return self

    def assert_metadata(self, metadata: dict) -> "Assertions":
        assert metadata["datasource"] == "confluence"
        assert metadata["format"] == "md"
        assert metadata["title"] == self.fixtures.page.title
        assert metadata["page_id"] == self.fixtures.page.id
        assert (
            metadata["created_time"] == self.fixtures.page.history.createdDate
        )
        assert (
            metadata["created_date"]
            == self.fixtures.page.history.createdDate.split("T")[0]
        )
        assert (
            metadata["last_edited_time"]
            == self.fixtures.page.history.lastUpdated.when.split("T")[0]
        )
        assert (
            metadata["last_edited_date"]
            == self.fixtures.page.history.lastUpdated.when
        )
        assert metadata["space"] == self.fixtures.space_name
        assert metadata["type"] == "page"
        assert (
            metadata["url"]
            == self.fixtures.base_url + self.fixtures.page.links.webui
        )
        return self

    def assert_markdown_parser_called(self) -> "Assertions":
        self.arrangements.markdown_parser.convert.assert_called_once_with(
            "temp_file.html", file_extension=".html"
        )
        return self

    def assert_markdown_parser_not_called(self) -> "Assertions":
        self.arrangements.markdown_parser.convert.assert_not_called()
        return self


class Manager:
    def __init__(self, arrangements: Arrangements):
        self.fixtures = arrangements.fixtures
        self.arrangements = arrangements
        self.assertions = Assertions(arrangements=arrangements)

    def get_service(self) -> ConfluenceDatasourceParser:
        return self.arrangements.service


class TestConfluenceDatasourceParser:
    def test_parse_confluence_page_to_document(self):
        # Arrange
        manager = Manager(
            Arrangements(
                Fixtures()
                .with_base_url()
                .with_configuration()
                .with_confluence_page()
                .with_markdown_content()
            )
            .on_parser_convert_return_markdown()
            .mock_tempfile()
        )
        service = manager.get_service()

        # Act
        document = service.parse(manager.fixtures.page)

        # Assert
        manager.assertions.assert_document_text(
            document
        ).assert_document_metadata(document).assert_markdown_parser_called()

        # Cleanup
        manager.arrangements.stop_patches()

    def test_parse_with_empty_content(self):
        # Arrange
        manager = Manager(
            Arrangements(
                Fixtures()
                .with_base_url()
                .with_configuration()
                .with_empty_content_page()
                .with_markdown_content()
            )
        )
        service = manager.get_service()

        # Act
        document = service.parse(manager.fixtures.page)

        # Assert
        manager.assertions.assert_empty_document_text(
            document
        ).assert_document_metadata(document).assert_markdown_parser_not_called()

    def test_extract_metadata(self):
        # Arrange
        manager = Manager(
            Arrangements(Fixtures().with_base_url().with_confluence_page())
        )

        # Act
        metadata = ConfluenceDatasourceParser._extract_metadata(
            manager.fixtures.page, manager.fixtures.base_url
        )

        # Assert
        manager.assertions.assert_metadata(metadata)
