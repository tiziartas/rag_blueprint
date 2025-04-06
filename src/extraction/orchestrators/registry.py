from core.base_factory import Registry
from extraction.bootstrap.configuration.configuration import OrchestratorName


class DatasourceOrchestratorRegistry(Registry):
    """
    Registry for datasource orchestrators.

    A specialized registry implementation that maps OrchestratorName enum values
    to their corresponding orchestrator factories.

    Attributes:
        _key_class: The class type used as registry keys, specifically OrchestratorName.
    """

    _key_class = OrchestratorName
