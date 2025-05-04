from typing import Type

from core.base_factory import Factory
from core.logger import LoggerConfiguration
from extraction.datasources.bundestag.client import BundestagSpeech
from extraction.datasources.bundestag.configuration import (
    BundestagMineDatasourceConfiguration,
)
from extraction.datasources.bundestag.document import BundestagMineDocument
from extraction.datasources.core.parser import BaseParser


class BundestagMineDatasourceParser(BaseParser[BundestagMineDocument]):

    logger = LoggerConfiguration.get_logger(__name__)

    def parse(self, speech: BundestagSpeech) -> BundestagMineDocument:
        """
        Parse content into a BundestagMineDocument object.

        Args:
            content: Raw response dict to be parsed

        Returns:
            Parsed document of type BundestagMineDocument
        """
        metadata = self._extract_metadata(speech)
        return BundestagMineDocument(text=speech.text, metadata=metadata)

    def _extract_metadata(self, speech: BundestagSpeech) -> dict:
        """
        Extract metadata from the response.

        Args:
            response: Raw response string

        Returns:
            Dictionary containing extracted metadata
        """
        legislature_period = speech.protocol.legislaturePeriod
        protocol_number = speech.protocol.number
        agenda_item_number = speech.agendaItem.agendaItemNumber

        url = f"https://dserver.bundestag.de/btp/{legislature_period}/{legislature_period}{protocol_number}.pdf"
        title = f"Protocol/Legislature/AgendaItem {protocol_number}/{legislature_period}/{agenda_item_number}"
        speaker_name = f"{speech.speaker.firstName} {speech.speaker.lastName}"

        return {
            "datasource": "bundestag",
            "language": "de",
            "url": url,
            "title": title,
            "format": "md",
            "created_time": speech.protocol.date,
            "last_edited_time": speech.protocol.date,
            "speaker_party": speech.speaker.party,
            "speaker": speaker_name,
            "agenda_item_number": agenda_item_number,
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
