from typing import Type

from core.base_factory import Factory
from extraction.datasources.bundestag.configuration import (
    BundestagMineDatasourceConfiguration,
)
from extraction.datasources.bundestag.document import BundestagMineDocument
from extraction.datasources.core.parser import BaseParser


class BundestagMineDatasourceParser(BaseParser[BundestagMineDocument]):

    def parse(self, response: str) -> BundestagMineDocument:
        """
        Parse content into a BundestagMineDocument object.

        Args:
            content: Raw response string to be parsed

        Returns:
            Parsed document of type BundestagMineDocument
        """
        markdown = response["text"]
        metadata = self._extract_metadata(response)
        return BundestagMineDocument(text=markdown, metadata=metadata)

    def _extract_metadata(self, response: str) -> dict:
        """
        Extract metadata from the response.

        Args:
            response: Raw response string

        Returns:
            Dictionary containing extracted metadata
        """
        legislature_period = response["legislaturePeriod"]
        protocol_number = response["protocolNumber"]
        url = f"https://dserver.bundestag.de/btp/{legislature_period}/{legislature_period}{protocol_number}.pdf"
        title = f"Protocol/Legislature {protocol_number}/{legislature_period}"
        speaker = f"{response['speaker']['firstName']} {response['speaker']['lastName']}"
        return {
            "datasource": "bundestag",
            "language": "de",
            "url": url,
            "title": title,
            "format": "md",
            "created_time": response["date"],
            "last_edited_time": response["date"],
            "speaker_party": response["speaker"]["party"],
            "speaker": speaker,
            "agenda_item_number": response["agendaItemNumber"],
            "protocol_number": protocol_number,
            "legislature_period": legislature_period,
        }


class BundestagMineDatasourceParserFactory(Factory):
    """
    Factory for creating instances of BundestagMineDatasourceParser.

    Creates and configures BundestagMineDatasourceParser objects according to
    the provided configuration.
    """

    _configuration_class: Type = BundestagMineDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: BundestagMineDatasourceConfiguration
    ) -> BundestagMineDatasourceParser:
        """
        Create an instance of BundestagMineDatasourceParser.

        Args:
            configuration: Configuration for the parser (not used in this implementation)

        Returns:
            An instance of BundestagMineDatasourceParser
        """
        return BundestagMineDatasourceParser()
