from typing import Type

from core import Registry
from embedding.bootstrap.configuration.configuration import EmbedderName


class EmbedderRegistry(Registry):
    _key_class: Type = EmbedderName
