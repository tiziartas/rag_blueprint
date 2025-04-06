from core.base_factory import Registry
from extraction.bootstrap.configuration.configuration import OrchestratorName


class DatasourceOrchestratorRegistry(Registry):
    _key_class = OrchestratorName
