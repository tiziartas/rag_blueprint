import os
from typing import Type

from llama_index.core.readers.file.base import default_file_metadata_func
from markitdown import MarkItDown

from core import Factory
from extraction.datasources.core.parser import BaseParser
from extraction.datasources.pdf.configuration import PDFDatasourceConfiguration
from extraction.datasources.pdf.document import PDFDocument


class PDFDatasourceParser(BaseParser[PDFDocument]):

    def __init__(self):
        """
        Attributes:
            parser: MarkItDown parser instance
        """
        self.parser = MarkItDown()

    def parse(self, file_path: str) -> PDFDocument:
        """
        Parses the given PDF file.
        Args:
            file_path (str): Path to the PDF file.
        Returns:
            PDFDocument: PDFDocument objects.
        """
        markdown = self.parser.convert(
            file_path, file_extension=".pdf"
        ).text_content
        metadata = self._extract_metadata(file_path)
        return PDFDocument(text=markdown, metadata=metadata)

    def _extract_metadata(self, file_path: str) -> dict:
        """Extract and process PDF metadata.
        Args:
            reader: PDF reader instance
        Returns:
            dict: Processed metadata dictionary
        """
        metadata = default_file_metadata_func(file_path)
        metadata.update(
            {
                "datasource": "pdf",
                "format": "pdf",
                "url": None,
                "title": os.path.basename(file_path),
                "last_edited_date": metadata["last_modified_date"],
                "created_date": metadata["creation_date"],
            }
        )
        del metadata["last_modified_date"]
        del metadata["creation_date"]
        return metadata


class PDFDatasourceParserFactory(Factory):
    _configuration_class: Type = PDFDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls, _: PDFDatasourceConfiguration
    ) -> PDFDatasourceParser:
        """
        Creates the default PDF parser.
        Returns:
            BasicPDFDatasourceParser: Default PDF parser instance
        """
        return PDFDatasourceParser()
