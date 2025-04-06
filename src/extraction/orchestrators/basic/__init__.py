from extraction.bootstrap.configuration.configuration import OrchestratorName
from extraction.orchestrators.basic.orchestrator import (
    BasicDatasourceOrchestratorFactory,
)
from extraction.orchestrators.registry import DatasourceOrchestratorRegistry


def register() -> None:
    DatasourceOrchestratorRegistry.register(
        OrchestratorName.BASIC, BasicDatasourceOrchestratorFactory
    )
