from typing import Type

from core import Registry
from extraction.bootstrap.configuration.datasources import DatasourceName


class DatasourceManagerRegistry(Registry):
    _key_class: Type = DatasourceName
