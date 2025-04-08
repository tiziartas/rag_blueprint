from typing import Type

from augmentation.bootstrap.initializer import AugmentationInitializer
from core.base_configuration import BaseConfiguration
from evaluation.bootstrap.configuration.configuration import (
    EvaluationConfiguration,
)


class EvaluationInitializer(AugmentationInitializer):
    """Initializer for evaluation processes that extends augmentation capabilities.

    This initializer inherits from AugmentationInitializer to reuse augmentation functionality
    while setting up evaluation-specific components. It handles the configuration binding
    and initialization of services required for evaluating RAG systems.

    The class bridges augmentation and evaluation processes by providing a consistent
    initialization pattern across the application. It's responsible for:
    - Loading evaluation configuration
    - Setting up evaluation metrics and benchmarks
    - Binding evaluation-specific dependencies
    """

    def __init__(
        self,
        configuration_class: Type[BaseConfiguration] = EvaluationConfiguration,
    ):
        """Initialize the evaluation components with the specified configuration.

        Args:
            configuration_class: Class to use for loading the evaluation configuration.
                Defaults to EvaluationConfiguration.
        """
        super().__init__(configuration_class)
