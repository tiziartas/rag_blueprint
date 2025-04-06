import argparse
import logging
import time
from abc import ABC
from enum import Enum
from typing import Any, Optional, Type

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    TypeAdapter,
    ValidationInfo,
    model_validator,
)
from pydantic_settings import BaseSettings

from core.base_factory import ConfigurationRegistry


class BaseConfiguration(BaseModel, ABC):

    def __hash__(self) -> int:
        """Not the most efficient way of hashing, but it works for now."""
        json = self.model_dump_json()
        return hash(json)

    @classmethod
    def _validate(
        cls,
        value: Any,
        info: ValidationInfo,
        registry: Type[ConfigurationRegistry],
    ) -> Any:
        """
        Function is invoked before the model is validated. It is used to validate the value of the field.
        If registry is defined in the field's metadata, it is used to validate the value.
        Otherwise, the value is returned as is.
        Args:
            value (Any): The value of the field.
            info (ValidationInfo): The information about the field.
        Returns:
            Any: The validated value.
        """
        type_adapter = TypeAdapter(registry.get_union_type())
        return type_adapter.validate_python(
            value,
            context=info.context,
        )


class BaseSecrets(BaseConfiguration, BaseSettings):
    model_config = ConfigDict(
        extra="ignore",
    )


class BaseConfigurationWithSecrets(BaseConfiguration):
    """
    Abstract model for configuration's secrets handling. Extending class has to implement `secrets` field with correspodning type.
    """

    secrets: BaseSecrets = Field(
        None,
        description="`EmptySecrets` is meant for the the configuration that does not require secrets."
        "In other case `EmptySecrets` should be replaced with the corresponding secrets class.",
    )

    def model_post_init(self, context: Any) -> None:
        """
        Function is invoked after the model is initialized. It is used to initialize secrets.

        Args:
            context (Any): The context passed to the pydantic model.
        """
        self.secrets = self._get_secrets(secrets_file=context["secrets_file"])

    def _get_secrets(self, secrets_file: str) -> BaseSettings:
        """
        Function to initialize secrets.

        Args:
            secrets_file (str): The path to the secrets file.

        Returns:
            BaseSettings: The secrets object.

        Raises:
            ValueError: If secrets are not found.
        """
        secrets_class = self.model_fields["secrets"].annotation
        secrets = secrets_class(_env_file=secrets_file)
        if secrets is None:
            raise ValueError(f"Secrets for {self.name} not found.")
        return secrets


class LogLevelName(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

    @property
    def value_as_int(self) -> int:
        """Convert string log level to the corresponding logging constant."""
        return logging._nameToLevel[self.value.upper()]


class EnvironmentName(str, Enum):
    DEFAULT = "default"
    LOCAL = "local"
    DEV = "dev"
    TEST = "test"
    PROD = "prod"


class MetadataConfiguration(BaseConfiguration):
    environment: EnvironmentName = Field(
        EnvironmentName.LOCAL,
        description="The environment of the application.",
    )
    build_name: Optional[str] = Field(
        None,
        description="The name of the build.",
    )
    log_level: LogLevelName = Field(
        LogLevelName.INFO, description="The log level of the application."
    )
    on_prem_config: bool = Field(
        False,
        description="If set, then the configuration will be read from on premise configuration."
        "Otherwise from the orchestrator service.",
    )

    @model_validator(mode="before")
    @classmethod
    def validate_from_args(cls, data: dict) -> dict:
        parser = cls._get_parser()
        args, _ = parser.parse_known_args()
        return cls._get_data(data=data, args=args)

    @classmethod
    def _get_data(cls, data: dict, args: argparse.Namespace) -> dict:
        """
        Function to parse the arguments.

        Returns:
            argparse.Namespace: The parsed arguments.
        """
        if args.env:
            data["environment"] = EnvironmentName(args.env)
        if args.build_name:
            data["build_name"] = args.build_name
        if args.on_prem_config:
            data["on_prem_config"] = args.on_prem_config
        if args.log_level:
            data["log_level"] = args.log_level

        return data

    @classmethod
    def _get_parser(cls) -> argparse.ArgumentParser:
        """
        Function to initialize the argument parser.

        Returns:
            argparse.ArgumentParser: The argument parser.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--env",
            type=EnvironmentName,
            help="Runtime environment.",
            default=EnvironmentName.LOCAL,
            choices=[env.value for env in EnvironmentName],
        )
        parser.add_argument(
            "--build-name",
            type=str,
            help="The name of the build.",
            default=f"build-local-{time.time()}",
        )
        parser.add_argument(
            "--on-prem-config",
            help="If set, then the configuration will be read from on premise configuration."
            "Otherwise from the orchestrator service.",
            action="store_true",
        )
        parser.add_argument(
            "--log-level",
            type=LogLevelName,
            help="Log level.",
            default=LogLevelName.INFO,
            choices=[level.value for level in LogLevelName],
        )
        return parser


class BasicConfiguration(BaseConfiguration):
    metadata: Optional[MetadataConfiguration] = Field(
        None, description="Metadata of the run."
    )
