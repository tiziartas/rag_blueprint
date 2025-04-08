import os
import sys
from typing import List
from unittest.mock import Mock, patch

import pytest

sys.path.append("./src")


from extraction.datasources.pdf.configuration import PDFDatasourceConfiguration
from extraction.datasources.pdf.reader import PDFDatasourceReader


class Fixtures:
    def __init__(self):
        self.export_limit: int = None
        self.base_path: str = None
        self.file_names: List[str] = []
        self.pdf_file_names: List[str] = []

    def with_export_limit(self, export_limit: int) -> "Fixtures":
        self.export_limit = export_limit
        return self

    def with_base_path(self) -> "Fixtures":
        self.base_path = "/fake/path"
        return self

    def with_pdf_files(self, number_of_files: int) -> "Fixtures":
        for i in range(number_of_files):
            file_name = f"document_{i}.pdf"
            self.file_names.append(file_name)
            self.pdf_file_names.append(file_name)
        return self

    def with_non_pdf_files(self, number_of_files: int) -> "Fixtures":
        for i in range(number_of_files):
            file_name = f"document_{i}.txt"
            self.file_names.append(file_name)
        return self


class Arrangements:
    def __init__(self, fixtures: Fixtures):
        self.fixtures = fixtures
        self.configuration = Mock(spec=PDFDatasourceConfiguration)
        self.configuration.export_limit = self.fixtures.export_limit
        self.configuration.base_path = self.fixtures.base_path
        self.service = PDFDatasourceReader(configuration=self.configuration)

    def on_os_listdir(self) -> "Arrangements":
        self.listdir_patcher = patch(
            "os.listdir", return_value=self.fixtures.file_names
        )
        self.mock_listdir = self.listdir_patcher.start()
        return self

    def on_pdf_document_creation(self) -> "Arrangements":
        def isfile_side_effect(path):
            return path.endswith(".pdf")

        self.isfile_patcher = patch(
            "os.path.isfile", side_effect=isfile_side_effect
        )

        self.mock_isfile = self.isfile_patcher.start()

        return self

    def stop_patches(self):
        self.listdir_patcher.stop()
        self.isfile_patcher.stop()


class Assertions:
    def __init__(self, arrangements: Arrangements):
        self.fixtures = arrangements.fixtures
        self.service = arrangements.service

    def assert_pdfs(self, pdf_file_paths: List[str]) -> "Assertions":
        for expected_file_name, actual_file_path in zip(
            self.fixtures.pdf_file_names, pdf_file_paths
        ):
            assert actual_file_path.endswith(expected_file_name)
            assert os.path.isfile(actual_file_path)


class Manager:
    def __init__(self, arrangements: Arrangements):
        self.fixtures = arrangements.fixtures
        self.arrangements = arrangements
        self.assertions = Assertions(arrangements=arrangements)

    def get_service(self) -> PDFDatasourceReader:
        return self.arrangements.service


class TestPdfReader:
    @pytest.mark.parametrize(
        "export_limit,number_of_pdfs,number_of_non_pdfs",
        [
            (5, 10, 5),
            (10, 15, 10),
            (None, 8, 2),
            (3, 5, 5),
            (20, 25, 5),
            (None, 0, 10),
            (5, 0, 10),
        ],
    )
    @pytest.mark.asyncio
    async def test(
        self, export_limit: int, number_of_pdfs: int, number_of_non_pdfs: int
    ) -> None:
        # Arrange
        manager = Manager(
            Arrangements(
                Fixtures()
                .with_export_limit(export_limit)
                .with_base_path()
                .with_non_pdf_files(number_of_non_pdfs)
                .with_pdf_files(number_of_pdfs)
            )
            .on_os_listdir()
            .on_pdf_document_creation()
        )
        service = manager.get_service()

        # Act
        pdf_file_paths = []
        async for pdf_file_path in service.read_all_async():
            pdf_file_paths.append(pdf_file_path)

        # Assert
        manager.assertions.assert_pdfs(pdf_file_paths)
