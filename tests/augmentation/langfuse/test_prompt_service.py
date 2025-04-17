import sys

sys.path.append("./src")

from unittest.mock import Mock

from langfuse.client import Langfuse

from augmentation.langfuse.prompt_service import LangfusePromptService


class Fixtures:
    def __init__(self):
        self.prompt_name: str = None
        self.prompt_template: str = None
        self.prompt_object = None

    def with_prompt_details(self) -> "Fixtures":
        self.prompt_name = "test_prompt"
        self.prompt_template = "This is a {test} prompt template"
        return self

    def with_prompt_object(self) -> "Fixtures":
        self.prompt_object = Mock()
        self.prompt_object.prompt = self.prompt_template
        return self


class Arrangements:
    def __init__(self, fixtures: Fixtures):
        self.fixtures = fixtures
        self.langfuse_client = Mock(spec=Langfuse)
        self.service = LangfusePromptService(client=self.langfuse_client)

    def on_prompt_exists(self) -> "Arrangements":
        self.langfuse_client.get_prompt.return_value = (
            self.fixtures.prompt_object
        )
        return self

    def on_prompt_does_not_exist(self) -> "Arrangements":
        self.langfuse_client.get_prompt.side_effect = Exception(
            "Prompt not found"
        )
        return self


class Assertions:
    def __init__(self, arrangements: Arrangements):
        self.fixtures = arrangements.fixtures
        self.arrangements = arrangements

    def assert_get_prompt_called(self) -> "Assertions":
        self.arrangements.langfuse_client.get_prompt.assert_called_once_with(
            self.fixtures.prompt_name
        )
        return self

    def assert_create_prompt_not_called(self) -> "Assertions":
        self.arrangements.langfuse_client.create_prompt.assert_not_called()
        return self

    def assert_create_prompt_called(self) -> "Assertions":
        self.arrangements.langfuse_client.create_prompt.assert_called_once_with(
            name=self.fixtures.prompt_name,
            prompt=self.fixtures.prompt_template,
            labels=["production"],
        )
        return self

    def assert_prompt_exists_result(self, result: bool) -> "Assertions":
        assert result is True
        return self

    def assert_prompt_not_exists_result(self, result: bool) -> "Assertions":
        assert result is False
        return self

    def assert_get_prompt_template_result(self, result: str) -> "Assertions":
        assert result == self.fixtures.prompt_template
        return self


class Manager:
    def __init__(self, arrangements: Arrangements):
        self.fixtures = arrangements.fixtures
        self.arrangements = arrangements
        self.assertions = Assertions(arrangements)

    def get_service(self) -> LangfusePromptService:
        return self.arrangements.service


class TestLangfusePromptService:
    def test_given_existing_prompt_when_create_if_not_exists_then_nothing_happens(
        self,
    ):
        # Arrange
        manager = Manager(
            Arrangements(
                Fixtures().with_prompt_details().with_prompt_object()
            ).on_prompt_exists()
        )
        service = manager.get_service()

        # Act
        service.create_prompt_if_not_exists(
            prompt_name=manager.fixtures.prompt_name,
            prompt_template=manager.fixtures.prompt_template,
        )

        # Assert
        manager.assertions.assert_get_prompt_called().assert_create_prompt_not_called()

    def test_given_non_existing_prompt_when_create_if_not_exists_then_prompt_is_created(
        self,
    ):
        # Arrange
        manager = Manager(
            Arrangements(
                Fixtures().with_prompt_details()
            ).on_prompt_does_not_exist()
        )
        service = manager.get_service()

        # Act
        service.create_prompt_if_not_exists(
            prompt_name=manager.fixtures.prompt_name,
            prompt_template=manager.fixtures.prompt_template,
        )

        # Assert
        manager.assertions.assert_get_prompt_called().assert_create_prompt_called()

    def test_given_existing_prompt_when_prompt_exists_then_returns_true(self):
        # Arrange
        manager = Manager(
            Arrangements(
                Fixtures().with_prompt_details().with_prompt_object()
            ).on_prompt_exists()
        )
        service = manager.get_service()

        # Act
        result = service.prompt_exists(prompt_name=manager.fixtures.prompt_name)

        # Assert
        manager.assertions.assert_get_prompt_called().assert_prompt_exists_result(
            result
        )

    def test_given_non_existing_prompt_when_prompt_exists_then_returns_false(
        self,
    ):
        # Arrange
        manager = Manager(
            Arrangements(
                Fixtures().with_prompt_details()
            ).on_prompt_does_not_exist()
        )
        service = manager.get_service()

        # Act
        result = service.prompt_exists(prompt_name=manager.fixtures.prompt_name)

        # Assert
        manager.assertions.assert_get_prompt_called().assert_prompt_not_exists_result(
            result
        )

    def test_given_existing_prompt_when_get_prompt_template_then_returns_template(
        self,
    ):
        # Arrange
        manager = Manager(
            Arrangements(
                Fixtures().with_prompt_details().with_prompt_object()
            ).on_prompt_exists()
        )
        service = manager.get_service()

        # Act
        result = service.get_prompt_template(
            prompt_name=manager.fixtures.prompt_name
        )

        # Assert
        manager.assertions.assert_get_prompt_called().assert_get_prompt_template_result(
            result
        )
