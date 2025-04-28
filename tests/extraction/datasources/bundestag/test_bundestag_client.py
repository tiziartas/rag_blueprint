import sys
from unittest.mock import Mock
from uuid import uuid4

from apiclient.exceptions import APIClientError, ResponseParseError

sys.path.append("./src")

from extraction.datasources.bundestag.client import BundestagMineClient


class Fixtures:
    def __init__(self):
        self.protocol_data = []
        self.agenda_items_data = {}
        self.speeches_data = {}
        self.speaker_data = {}

    def with_protocols(self, count: int = 3) -> "Fixtures":
        self.protocol_data = [
            {
                "id": str(uuid4()),
                "legislaturePeriod": f"{i+19}",
                "number": f"{i+100}",
            }
            for i in range(count)
        ]
        return self

    def with_agenda_items(self, items_per_protocol: int = 2) -> "Fixtures":
        for protocol in self.protocol_data:
            protocol_id = protocol["id"]
            self.agenda_items_data[protocol_id] = {
                "agendaItems": [
                    {
                        "id": str(uuid4()),
                        "agendaItemNumber": f"{i+1}",
                        "title": f"Agenda Item {i+1}",
                    }
                    for i in range(items_per_protocol)
                ]
            }
        return self

    def with_speeches(self, speeches_per_item: int = 2) -> "Fixtures":
        for protocol in self.protocol_data:
            wp = int(protocol["legislaturePeriod"])
            num = int(protocol["number"])

            for agenda_items in self.agenda_items_data.values():
                for item in agenda_items["agendaItems"]:
                    ain = item["agendaItemNumber"]
                    key = f"{wp},{num},{ain}"

                    self.speeches_data[key] = {
                        "speeches": [
                            {
                                "id": str(uuid4()),
                                "speakerId": f"speaker_{i}",
                                "text": f"Speech {i} content",
                            }
                            for i in range(speeches_per_item)
                        ]
                    }
        return self

    def with_speaker_data(self) -> "Fixtures":
        # Create speaker data for each speech
        for speech_group in self.speeches_data.values():
            for speech in speech_group["speeches"]:
                speaker_id = speech["speakerId"]
                self.speaker_data[speaker_id] = {
                    "id": speaker_id,
                    "name": f"Speaker {speaker_id}",
                    "party": "Test Party",
                }
        return self


class Arrangements:
    def __init__(self, fixtures: Fixtures) -> None:
        self.fixtures = fixtures
        self.client = BundestagMineClient()

    def mock_safe_get(self) -> "Arrangements":
        def mock_safe_get_side_effect(path: str):
            if path == "GetProtocols":
                return self.fixtures.protocol_data

            if path.startswith("GetAgendaItemsOfProtocol/"):
                protocol_id = path.split("/")[1]
                return self.fixtures.agenda_items_data.get(
                    protocol_id, {"agendaItems": []}
                )

            if path.startswith("GetSpeechesOfAgendaItem/"):
                key = path.split("/")[1]
                import urllib.parse

                key = urllib.parse.unquote(key)
                return self.fixtures.speeches_data.get(key, {"speeches": []})

            if path.startswith("GetSpeakerById/"):
                speaker_id = path.split("/")[1]
                return self.fixtures.speaker_data.get(speaker_id, {})

            return {}

        self.client.safe_get = Mock(side_effect=mock_safe_get_side_effect)
        return self

    def with_failing_protocols(self) -> "Arrangements":
        self.client.safe_get = Mock(side_effect=APIClientError("API Error"))
        return self

    def with_failing_agenda_items(self) -> "Arrangements":
        original_safe_get = self.client.safe_get

        def mock_with_fail(path: str):
            if path.startswith("GetAgendaItemsOfProtocol/"):
                raise ResponseParseError("Parse Error")
            return original_safe_get(path)

        self.client.safe_get = Mock(side_effect=mock_with_fail)
        return self

    def with_failing_speeches(self) -> "Arrangements":
        original_safe_get = self.client.safe_get

        def mock_with_fail(path: str):
            if path.startswith("GetSpeechesOfAgendaItem/"):
                raise APIClientError("API Error")
            return original_safe_get(path)

        self.client.safe_get = Mock(side_effect=mock_with_fail)
        return self


class Assertions:
    def __init__(self, arrangements: Arrangements) -> None:
        self.fixtures = arrangements.fixtures
        self.arrangements = arrangements
        self.client = arrangements.client

    def assert_protocols(self, protocols):
        assert protocols == self.fixtures.protocol_data

    def assert_agenda_items(self, protocol_id, agenda_items):
        expected = self.fixtures.agenda_items_data.get(
            protocol_id, {"agendaItems": []}
        ).get("agendaItems", [])
        assert agenda_items == expected

    def assert_speeches(self, speeches, wp, num, ain):
        key = f"{wp},{num},{ain}"
        expected_speeches = self.fixtures.speeches_data.get(
            key, {"speeches": []}
        ).get("speeches", [])

        for speech in speeches:
            if "speakerId" in speech:
                assert "speaker" in speech
                assert speech["speaker"] == self.fixtures.speaker_data.get(
                    speech["speakerId"], {}
                )

        speech_ids = [s["id"] for s in speeches]
        expected_ids = [s["id"] for s in expected_speeches]
        assert set(speech_ids) == set(expected_ids)

    def assert_all_speeches(self, all_speeches_iterator):
        all_speeches = list(all_speeches_iterator)

        expected_count = 0
        for speech_group in self.fixtures.speeches_data.values():
            expected_count += len(speech_group["speeches"])

        assert len(all_speeches) <= expected_count

        for speech in all_speeches:
            if "speakerId" in speech:
                assert "speaker" in speech


class Manager:
    def __init__(self, arrangements: Arrangements):
        self.fixtures = arrangements.fixtures
        self.arrangements = arrangements
        self.assertions = Assertions(arrangements=arrangements)

    def get_client(self) -> BundestagMineClient:
        return self.arrangements.client


class TestBundestagMineClient:
    def test_get_protocols(self):
        # Arrange
        manager = Manager(
            Arrangements(Fixtures().with_protocols()).mock_safe_get()
        )
        client = manager.get_client()

        # Act
        protocols = client.get_protocols()

        # Assert
        manager.assertions.assert_protocols(protocols)

    def test_get_agenda_items(self):
        # Arrange
        fixtures = Fixtures().with_protocols().with_agenda_items()
        manager = Manager(Arrangements(fixtures).mock_safe_get())
        client = manager.get_client()
        protocol_id = fixtures.protocol_data[0]["id"]

        # Act
        agenda_items = client.get_agenda_items(protocol_id)

        # Assert
        manager.assertions.assert_agenda_items(protocol_id, agenda_items)

    def test_get_speeches(self):
        # Arrange
        fixtures = (
            Fixtures()
            .with_protocols()
            .with_agenda_items()
            .with_speeches()
            .with_speaker_data()
        )
        manager = Manager(Arrangements(fixtures).mock_safe_get())
        client = manager.get_client()
        wp = int(fixtures.protocol_data[0]["legislaturePeriod"])
        num = int(fixtures.protocol_data[0]["number"])
        ain = fixtures.agenda_items_data[fixtures.protocol_data[0]["id"]][
            "agendaItems"
        ][0]["agendaItemNumber"]

        # Act
        speeches = client.get_speeches(wp, num, ain)

        # Assert
        manager.assertions.assert_speeches(speeches, wp, num, ain)

    def test_fetch_all_speeches(self):
        # Arrange
        fixtures = (
            Fixtures()
            .with_protocols()
            .with_agenda_items()
            .with_speeches()
            .with_speaker_data()
        )
        manager = Manager(Arrangements(fixtures).mock_safe_get())
        client = manager.get_client()

        # Act
        all_speeches_iterator = client.fetch_all_speeches()

        # Assert
        manager.assertions.assert_all_speeches(all_speeches_iterator)

    def test_fetch_all_speeches_with_failing_protocols(self):
        manager = Manager(Arrangements(Fixtures()).with_failing_protocols())
        client = manager.get_client()

        all_speeches_iterator = client.fetch_all_speeches()

        all_speeches = list(all_speeches_iterator)
        assert all_speeches == []

    def test_fetch_all_speeches_with_failing_agenda_items(self):
        fixtures = Fixtures().with_protocols()
        manager = Manager(
            Arrangements(fixtures).mock_safe_get().with_failing_agenda_items()
        )
        client = manager.get_client()

        all_speeches_iterator = client.fetch_all_speeches()

        all_speeches = list(all_speeches_iterator)
        assert all_speeches == []

    def test_fetch_all_speeches_with_failing_speeches(self):
        fixtures = Fixtures().with_protocols().with_agenda_items()
        manager = Manager(
            Arrangements(fixtures).mock_safe_get().with_failing_speeches()
        )
        client = manager.get_client()

        all_speeches_iterator = client.fetch_all_speeches()

        all_speeches = list(all_speeches_iterator)
        assert all_speeches == []
