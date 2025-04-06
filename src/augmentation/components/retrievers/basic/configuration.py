from typing import Literal

from pydantic import Field

from augmentation.bootstrap.configuration.components.retriever_configuration import (
    RetrieverConfiguration,
    RetrieverName,
)


class BasicRetrieverConfiguration(RetrieverConfiguration):
    """
    Configuration for the Basic Retriever component.

    This class defines the configuration parameters needed for initializing
    and operating the basic retriever, extending the base RetrieverConfiguration.
    """

    name: Literal[RetrieverName.BASIC] = Field(
        ..., description="The name of the retriever."
    )
