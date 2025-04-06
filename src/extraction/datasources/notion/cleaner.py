import re

from bs4 import BeautifulSoup
from markdownify import markdownify as md

from core.base_factory import Factory
from extraction.datasources.core.cleaner import BasicMarkdownCleaner
from extraction.datasources.notion.configuration import (
    NotionDatasourceConfiguration,
)
from extraction.datasources.notion.document import NotionDocument


class NotionDatasourceCleaner(BasicMarkdownCleaner[NotionDocument]):
    """Cleaner for Notion document content.

    Implements cleaning logic for Notion databases and pages, removing HTML
    tags and comments while preserving meaningful content.

    Note:
        Expects documents to be in markdown format.
    """

    def clean(self, document: NotionDocument) -> NotionDocument:
        """Clean a collection of Notion documents.

        Processes both databases and pages, removing HTML artifacts and empty content.

        Args:
            documents: Collection of Notion documents to clean

        Returns:
            List[NotionDocument]: Filtered and cleaned documents
        """
        if document.metadata["type"] == "database":
            cleaned_text = self._clean_database(document)
            document.set_content(cleaned_text)
        if document.metadata["type"] == "page":
            cleaned_text = self._clean_page(document)
            document.set_content(cleaned_text)

        if self._has_empty_content(document):
            return None

        return document

    def _clean_database(self, document: NotionDocument) -> str:
        """Clean Notion database content.

        Args:
            document: Database document to clean

        Returns:
            str: Cleaned database content
        """
        return NotionDatasourceCleaner._parse_html_in_markdown(document.text)

    def _clean_page(self, document: NotionDocument) -> str:
        """Clean Notion page content.

        Args:
            document: Page document to clean

        Returns:
            str: Cleaned page content
        """
        return NotionDatasourceCleaner._parse_html_in_markdown(document.text)

    @staticmethod
    def _parse_html_in_markdown(md_text: str) -> str:
        """Process HTML elements within markdown content.

        Converts HTML to markdown and removes content without alphanumeric characters.

        Args:
            md_text: Text containing markdown and HTML

        Returns:
            str: Cleaned markdown text

        Note:
            Uses BeautifulSoup for HTML parsing
        """

        def replace_html(match):
            html_content = match.group(0)
            soup = BeautifulSoup(html_content, "html.parser")
            markdown = md(str(soup))

            if not re.search(r"[a-zA-Z0-9]", markdown):
                return ""
            return markdown

        md_text = re.sub(r"<!--.*?-->", "", md_text, flags=re.DOTALL)
        html_block_re = re.compile(r"<.*?>", re.DOTALL)
        return re.sub(html_block_re, replace_html, md_text)


class NotionDatasourceCleanerFactory(Factory):
    """Factory for creating NotionDatasourceCleaner instances.

    This factory is responsible for creating instances of NotionDatasourceCleaner
    with the appropriate configuration.
    """

    _configuration_class = NotionDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls, _: NotionDatasourceConfiguration
    ) -> NotionDatasourceCleaner:
        """Create a new instance of NotionDatasourceCleaner.

        Args:
            configuration: Configuration for the cleaner

        Returns:
            NotionDatasourceCleaner: Instance of NotionDatasourceCleaner
        """
        return NotionDatasourceCleaner()
