import sys

sys.path.append("./src")

import textwrap

from llama_index.core import Document

from extraction.datasources.notion.cleaner import NotionDatasourceCleaner
from extraction.datasources.notion.document import NotionDocument


class Fixtures:

    def __init__(self):
        self.notion_document: NotionDocument = []
        self.notion_cleaned_document: NotionDocument = []

    def with_database_document(self) -> "Fixtures":
        self.notion_document = NotionDocument(
            text=textwrap.dedent(
                """
                This is a database document
                <!-- With HTML comment -->
                <div>
                    <p>And some HTML content</p>
                </div>
                As well as normal text
            """
            ),
            metadata={"type": "page"},
        )

        self.notion_cleaned_document = NotionDocument(
            text=textwrap.dedent(
                """
                This is a database document


                    And some HTML content

                As well as normal text
            """
            ),
            metadata={"type": "page"},
        )

        return self

    def with_page_document(self) -> "Fixtures":
        self.notion_document = NotionDocument(
            text=textwrap.dedent(
                """
                This is a database document
                <!-- With HTML comment -->
                <div attr="value">
                    <a attr="href">And some HTML content</a>
                </div>
                As well as normal text
            """
            ),
            metadata={"type": "page"},
        )

        self.notion_cleaned_document = NotionDocument(
            text=textwrap.dedent(
                """
                This is a database document


                    And some HTML content

                As well as normal text
            """
            ),
            metadata={"type": "page"},
        )

        return self

    def with_empty_document(self) -> "Fixtures":
        self.notion_document = NotionDocument(
            text=" \n   \t\n\t ", metadata={"type": "page"}
        )
        self.notion_cleaned_document = None

        return self


class Arrangements:

    def __init__(self, fixtures: Fixtures) -> None:
        self.fixtures = fixtures

        self.service = NotionDatasourceCleaner()


class Assertions:

    def __init__(self, arrangements: Arrangements) -> None:
        self.fixtures = arrangements.fixtures
        self.arrangements = arrangements
        self.service = arrangements.service

    def assert_cleaned_document(self, cleaned_document: Document) -> None:
        if self.fixtures.notion_cleaned_document is None:
            assert cleaned_document is None
        else:
            assert (
                cleaned_document.text
                == self.fixtures.notion_cleaned_document.text
            )


class Manager:

    def __init__(self, arrangements: Arrangements):
        self.fixtures = arrangements.fixtures
        self.arrangements = arrangements
        self.assertions = Assertions(arrangements=arrangements)

    def get_service(self) -> NotionDatasourceCleaner:
        return self.arrangements.service


class TestNotionDatasourceCleaner:

    def test_given_database_document_when_clean_then_document_is_cleaned(self):
        # Arrange
        manager = Manager(
            Arrangements(
                Fixtures().with_database_document(),
            ),
        )
        service = manager.get_service()

        # Act
        cleaned_document = service.clean(manager.fixtures.notion_document)

        # Assert
        manager.assertions.assert_cleaned_document(cleaned_document)

    def test_given_page_document_when_clean_then_document_is_cleaned(self):
        # Arrange
        manager = Manager(
            Arrangements(
                Fixtures().with_page_document(),
            ),
        )
        service = manager.get_service()

        # Act
        cleaned_document = service.clean(manager.fixtures.notion_document)

        # Assert
        manager.assertions.assert_cleaned_document(cleaned_document)

    def test_given_empty_document_when_clean_then_document_is_not_cleaned(
        self,
    ):
        # Arrange
        manager = Manager(
            Arrangements(
                Fixtures().with_empty_document(),
            ),
        )
        service = manager.get_service()

        # Act
        cleaned_document = service.clean(manager.fixtures.notion_document)

        # Assert
        manager.assertions.assert_cleaned_document(cleaned_document)
