from typing import Type

from core import Registry
from embedding.bootstrap.configuration.splitting_configuration import (
    SplitterName,
)


class SplitterRegistry(Registry):
    _key_class: Type = SplitterName
