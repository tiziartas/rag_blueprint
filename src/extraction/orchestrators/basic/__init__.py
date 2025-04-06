from extraction.bootstrap.configuration.configuration import OrchestratorName
from extraction.orchestrators.basic.orchestrator import (
    BasicDatasourceOrchestratorFactory,
)
from extraction.orchestrators.registry import DatasourceOrchestratorRegistry


def register() -> None:
    """
    Registers the BasicDatasourceOrchestratorFactory in the DatasourceOrchestratorRegistry.
    This function is called when the module is imported.
    """
    DatasourceOrchestratorRegistry.register(
        OrchestratorName.BASIC, BasicDatasourceOrchestratorFactory
    )
