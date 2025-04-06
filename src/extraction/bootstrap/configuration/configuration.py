from enum import Enum
from typing import Any, List

from pydantic import Field, ValidationInfo, field_validator

from core import BaseConfiguration, BasicConfiguration
from extraction.bootstrap.configuration.datasources import (
    DatasourceConfigurationRegistry,
)


class OrchestratorName(str, Enum):
    """
    Enum representing the available orchestrators for extraction.
    """

    BASIC = "basic"


class _ExtractionConfiguration(BaseConfiguration):
    """
    Configuration class for extraction settings.
    Defines the orchestrator and data sources to be used.
    """

    orchestrator_name: OrchestratorName = Field(
        OrchestratorName.BASIC, description="The orchestrator name."
    )
    datasources: List[Any] = Field(
        ...,
        description="Datasources configuration. Types are dynamically validated against configurations registered in `DatasourceConfigurationRegistry`.",
    )

    @field_validator("datasources")
    @classmethod
    def _validate_datasources(
        cls, value: List[Any], info: ValidationInfo
    ) -> List[Any]:
        """
        Validates the datasources configuration against registered configuration schemas.

        Args:
            value: List of datasource configurations to validate
            info: Validation context information

        Returns:
            List of validated datasource configuration objects
        """
        return super()._validate(
            value,
            info=info,
            registry=DatasourceConfigurationRegistry,
        )


class ExtractionConfiguration(BasicConfiguration):
    """
    Main configuration class for the extraction system.
    Extends the BasicConfiguration with extraction-specific settings.
    """

    extraction: _ExtractionConfiguration = Field(
        ..., description="Extraction configuration."
    )
