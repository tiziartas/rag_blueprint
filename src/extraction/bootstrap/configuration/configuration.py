from enum import Enum
from typing import Any, List

from pydantic import Field, ValidationInfo, field_validator

from core import BaseConfiguration, BasicConfiguration
from extraction.bootstrap.configuration.datasources import (
    DatasourceConfigurationRegistry,
)


class OrchestratorName(str, Enum):
    BASIC = "basic"


class _ExtractionConfiguration(BaseConfiguration):
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
        return super()._validate(
            value,
            info=info,
            registry=DatasourceConfigurationRegistry,
        )


class ExtractionConfiguration(BasicConfiguration):
    extraction: _ExtractionConfiguration = Field(
        ..., description="Extraction configuration."
    )
