from typing import Type

from augmentation.bootstrap.initializer import AugmentationInitializer
from core.base_configuration import BaseConfiguration
from evaluation.bootstrap.configuration.configuration import (
    EvaluationConfiguration,
)


class EvaluationInitializer(AugmentationInitializer):
    """Common initializer for embedding, augmentation and evaluation processes.

    Multiple components are used in the embedding, augmentation and evaluation processes.
    To avoid code duplication, this initializer is used to bind the components to the injector.
    It is intended to be subclassed by the specific initializers for each process.

    Attributes:
        configuration: Configuration object
        configuration_json: Configuration JSON string
    """

    def __init__(
        self,
        configuration_class: Type[BaseConfiguration] = EvaluationConfiguration,
    ):
        super().__init__(configuration_class)
