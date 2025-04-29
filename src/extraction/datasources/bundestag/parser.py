from typing import Optional, Type

from core.base_factory import Factory
from core.logger import LoggerConfiguration
from extraction.datasources.bundestag.configuration import (
    BundestagMineDatasourceConfiguration,
)
from extraction.datasources.bundestag.document import BundestagMineDocument
from extraction.datasources.core.parser import BaseParser


class BundestagMineDatasourceParser(BaseParser[BundestagMineDocument]):

    logger = LoggerConfiguration.get_logger(__name__)

    def parse(self, response: dict) -> Optional[BundestagMineDocument]:
        """
        Parse content into a BundestagMineDocument object. If parsing fails,
        return None and log an error message.

        Args:
            content: Raw response dict to be parsed

        Returns:
            Parsed document of type BundestagMineDocument
        """
        if "text" not in response:
            self.logger.error("Response does not contain 'text' field.")
            return None

        markdown = response["text"]
        metadata = self._extract_metadata(response)

        if metadata is None:
            self.logger.error("Failed to extract metadata from the response.")
            return None

        return BundestagMineDocument(text=markdown, metadata=metadata)

    def _extract_metadata(self, response: dict) -> Optional[dict]:
        """
        Extract metadata from the response. In case of an error, return an empty dictionary.

        Args:
            response: Raw response string

        Returns:
            Dictionary containing extracted metadata
        """
        try:
            legislature_period = response["legislaturePeriod"]
            protocol_number = response["protocolNumber"]
            agenda_item_number = response["agendaItemNumber"]
            speaker = response["speaker"]

            url = f"https://dserver.bundestag.de/btp/{legislature_period}/{legislature_period}{protocol_number}.pdf"
            title = f"Protocol/Legislature/AgendaItem {protocol_number}/{legislature_period}/{agenda_item_number}"
            speaker_name = f"{speaker['firstName']} {speaker['lastName']}"
            return {
                "datasource": "bundestag",
                "language": "de",
                "url": url,
                "title": title,
                "format": "md",
                "created_time": response["date"],
                "last_edited_time": response["date"],
                "speaker_party": speaker["party"],
                "speaker": speaker_name,
                "agenda_item_number": agenda_item_number,
                "protocol_number": protocol_number,
                "legislature_period": legislature_period,
            }
        except Exception as e:
            self.logger.error(f"Error extracting speech's metadata: {str(e)}")
            return None


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
