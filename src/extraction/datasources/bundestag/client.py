from urllib.parse import quote
from typing import Any, Dict, List

from apiclient import APIClient, retry_request
from apiclient.exceptions import APIClientError, ResponseParseError


# TODO: eventually refactor this to use async, HTTPX and tenacity
class BundestagMineClient(APIClient):
    """
    API Client for the bundestag-mine.de API.
    """

    BASE_URL = "https://bundestag-mine.de/api/DashboardController"

    def safe_get(self, path: str) -> Dict[str, Any]:
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
            raise ResponseParseError(f"HTTP error for {url}: {e}")

        data = resp.json()
        if not isinstance(data, dict) or data.get("status") != "200":
            raise ResponseParseError(f"Unexpected response for {url}: {data}")

        result = data.get("result")
        if result is None:
            return {}
        return result

    def get_protocols(self) -> List[Dict[str, Any]]:
        """
        Fetches the list of all protocols.

        Returns:
            List[Dict[str, Any]]: A list of protocols.
        """
        result = self.safe_get("GetProtocols")
        if not isinstance(result, list):
            raise ResponseParseError(f"Expected list of protocols, got: {result}")
        return result

    def get_agenda_items(self, protocol_id: str) -> List[Dict[str, Any]]:
        """
        Fetches agenda items for a specific protocol ID.

        Args:
            protocol_id (str): The ID of the protocol.

        Returns:
            List[Dict[str, Any]]: A list of agenda items.
        """
        result = self.safe_get(f"GetAgendaItemsOfProtocol/{protocol_id}")
        items = result.get("agendaItems")
        if items is None:
            return []
        if not isinstance(items, list):
            raise ResponseParseError(
                f"Expected list of agendaItems for {protocol_id}, got: {items}"
            )
        return items

    def get_speaker_data(self, speaker_id: str) -> Dict[str, Any]:
        """ """
        result = self.safe_get(f"GetSpeakerById/{speaker_id}")
        if not isinstance(result, dict):
            raise ResponseParseError(f"Expected speaker data, got: {result}")
        return result

    @retry_request
    def get_speeches(
        self, legislature_period: int, protocol_number: int, agenda_item_number: str
    ) -> List[Dict[str, Any]]:
        """
        Fetches speeches for a specific agenda item within a protocol.

        Args:
            legislature_period (int): The legislature period.
            protocol_number (int): The protocol number.
            agenda_item_number (str): The agenda item number.

        Returns:
            List[Dict[str, Any]]: A list of speeches.
        """
        raw = f"{legislature_period},{protocol_number},{agenda_item_number}"
        encoded = quote(raw, safe="")
        result = self.safe_get(f"GetSpeechesOfAgendaItem/{encoded}")
        speeches = result.get("speeches")
        if speeches is None:
            return []
        if not isinstance(speeches, list):
            raise ResponseParseError(
                f"Expected list of speeches for {raw}, got: {speeches}"
            )

        # add speaker data
        for speech in speeches:
            speaker_id = speech.get("speakerId")
            if speaker_id is None:
                continue
            try:
                speaker_data = self.get_speaker_data(speaker_id)
                speech["speaker"] = speaker_data
            except (APIClientError, ResponseParseError):
                continue

        return speeches

    def fetch_all_speeches(self) -> List[Dict[str, Any]]:
        """
        Fetches all speeches by iterating through protocols and their agenda items.

        Returns:
            List[Dict[str, Any]]: A list containing all speeches found.
        """
        try:
            protocols = self.get_protocols()
        except (APIClientError, ResponseParseError) as e:
            return []

        all_speeches: List[Dict[str, Any]] = []

        for prot in protocols[:1]:
            pid = prot.get("id")
            wp = prot.get("legislaturePeriod")
            num = prot.get("number")
            if not pid or wp is None or num is None:
                continue  # skip incomplete entries

            # normalize types
            try:
                wp_int = int(wp)
                num_int = int(num)
            except (ValueError, TypeError):
                continue

            # get agenda items
            try:
                items = self.get_agenda_items(pid)
            except (APIClientError, ResponseParseError):
                continue

            for item in items:
                ain = item.get("agendaItemNumber")
                if ain is None:
                    continue
                try:
                    speeches = self.get_speeches(wp_int, num_int, str(ain))
                    all_speeches.extend(speeches)
                except (APIClientError, ResponseParseError):
                    continue

        return all_speeches
