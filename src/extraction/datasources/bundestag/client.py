from typing import Any, Iterator, Optional, Type
from urllib.parse import quote

from apiclient import APIClient, retry_request
from apiclient.exceptions import ResponseParseError
from pydantic import BaseModel, ValidationError, model_validator

from core import SingletonFactory
from core.logger import LoggerConfiguration
from extraction.datasources.bundestag.configuration import (
    BundestagMineDatasourceConfiguration,
)


class Speaker(BaseModel):
    id: str
    firstName: str
    lastName: str
    party: str


class AgendaItem(BaseModel):
    id: str
    agendaItemNumber: str
    title: Optional[str] = None


class Protocol(BaseModel):
    id: str
    legislaturePeriod: int
    number: int
    date: Optional[str] = None


class Speech(BaseModel):
    id: str
    speakerId: str
    text: str
    speaker: Optional[Speaker] = None
    protocol: Optional[Protocol] = None
    agendaItem: Optional[AgendaItem] = None

    @model_validator(mode="after")
    def validate_text_not_empty(self) -> "Speech":
        if not self.text or self.text.strip() == "":
            raise ValueError("Speech text cannot be empty")
        return self


# TODO: eventually refactor this to use async, HTTPX and tenacity
class BundestagMineClient(APIClient):
    """
    API Client for the bundestag-mine.de API.
    """

    BASE_URL = "https://bundestag-mine.de/api/DashboardController"
    logger = LoggerConfiguration.get_logger(__name__)

    def safe_get(self, path: str) -> Optional[Any]:
        """
        Perform a GET request, raise for HTTP errors, parse JSON, check API status.

        Args:
            path: endpoint path under BASE_URL, e.g. "GetProtocols" or
                  "GetAgendaItemsOfProtocol/<protocol_id>"

        Returns:
            Dict[str, Any]: The 'result' field of the API response as a dict.

        Raises:
            ResponseParseError: if HTTP status is not OK or unexpected JSON structure.
        """
        url = f"{self.BASE_URL}/{path.lstrip('/')}"
        resp = self.get(url)
        try:
            resp.raise_for_status()
        except Exception as e:
            self.logger.error(f"HTTP error for {url}: {e}")
            return None

        data = resp.json()
        if not isinstance(data, dict) or data.get("status") != "200":
            self.logger.error(f"Unexpected response for {url}: {data}")
            return None

        result = data.get("result")
        if result is None:
            self.logger.debug(f"No result found for {url}")
            return None

        return result

    def get_protocols(self) -> Iterator[Protocol]:
        """
        Fetches the list of all protocols.

        Returns:
            Iterator[Protocol]: An iterator of valid protocols as Pydantic models.
        """
        result = self.safe_get("GetProtocols")
        if not isinstance(result, list):
            raise ResponseParseError(
                f"Expected list of protocols, got: {result}"
            )

        for protocol_data in result:
            try:
                yield Protocol.model_validate(protocol_data)
            except ValidationError as e:
                self.logger.warning(
                    f"Failed to validate protocol: {protocol_data}. Error: {e}"
                )

    def get_agenda_items(self, protocol_id: str) -> Iterator[AgendaItem]:
        """
        Fetches agenda items for a specific protocol ID.

        Args:
            protocol_id (str): The ID of the protocol.

        Returns:
            Iterator[AgendaItem]: An iterator of valid agenda items as Pydantic models.
        """
        result = self.safe_get(f"GetAgendaItemsOfProtocol/{protocol_id}")
        items = result.get("agendaItems")

        if items is None:
            self.logger.debug(f"No agenda items found for {protocol_id}")
            return
        if not isinstance(items, list):
            self.logger.error(
                f"Expected list of agendaItems for {protocol_id}, got: {items}"
            )
            return

        for item_data in items:
            try:
                yield AgendaItem.model_validate(item_data)
            except ValidationError as e:
                self.logger.warning(
                    f"Failed to validate agenda item: {item_data}. Error: {e}"
                )

    def get_speaker_data(self, speaker_id: str) -> Optional[Speaker]:
        """
        Fetches speaker data for a specific speaker ID.

        Args:
            speaker_id (str): The ID of the speaker.

        Returns:
            Optional[Speaker]: Speaker data as a Pydantic model, or None if validation fails.
        """
        result = self.safe_get(f"GetSpeakerById/{speaker_id}")
        if not isinstance(result, dict):
            self.logger.error(
                f"Expected speaker data for {speaker_id}, got: {result}"
            )
            return None

        try:
            return Speaker.model_validate(result)
        except ValidationError as e:
            self.logger.warning(
                f"Failed to validate speaker data for {speaker_id}: {result}. Error: {e}"
            )
            return None

    @retry_request
    def get_speeches(
        self,
        protocol: Protocol,
        agenda_item: AgendaItem,
    ) -> Iterator[Speech]:
        """
        Fetches speeches for a specific agenda item within a protocol.

        Args:
            legislature_period (int): The legislature period.
            protocol_number (int): The protocol number.
            agenda_item_number (str): The agenda item number.

        Returns:
            Iterator[Speech]: An iterator of valid speeches as Pydantic models.
        """
        raw = f"{protocol.legislaturePeriod},{protocol.number},{agenda_item.agendaItemNumber}"
        encoded = quote(raw, safe="")
        result = self.safe_get(f"GetSpeechesOfAgendaItem/{encoded}")

        if result is None:
            self.logger.debug(f"No speeches found for {raw}")
            return

        speeches = result.get("speeches")
        if speeches is None:
            self.logger.debug(f"No speeches found for {raw}")
            return

        if not isinstance(speeches, list):
            self.logger.warning(
                f"Expected list of speeches for {raw}, got: {speeches}"
            )
            return

        for speech in speeches:
            try:
                speech = Speech.model_validate(speech)
                speech.protocol = protocol
                speech.agendaItem = agenda_item
                yield speech
            except ValidationError as e:
                self.logger.warning(
                    f"Failed to validate speech: {speech}. Error: {e}"
                )

    def fetch_all_speeches(self) -> Iterator[Speech]:
        """
        Fetches all speeches by iterating through protocols and their agenda items.

        Returns:
            Iterator[Speech]: An iterator of valid speeches as Pydantic models.
        """
        for protocol in self.get_protocols():
            self.logger.info(f"Processing protocol {protocol.id}")

            for agenda_item in self.get_agenda_items(protocol.id):

                for speech in self.get_speeches(
                    protocol=protocol,
                    agenda_item=agenda_item,
                ):
                    speaker = self.get_speaker_data(speech.speakerId)
                    if speaker:
                        speech.speaker = speaker
                        yield speech


class BundestagMineClientFactory(SingletonFactory):
    """
    Factory for creating and managing Bundestag client instances.

    This factory ensures only one Bundestag client is created per configuration,
    following the singleton pattern provided by the parent SingletonFactory class.
    """

    _configuration_class: Type = BundestagMineDatasourceConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: BundestagMineDatasourceConfiguration
    ) -> BundestagMineClient:
        """
        Creates a new BundestagMine client instance using the provided configuration.

        Args:
            configuration: Configuration object containing BundestagMine details

        Returns:
            A configured BundestagMine client instance ready for API interactions.
        """
        return BundestagMineClient()
