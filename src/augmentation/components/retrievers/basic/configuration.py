from typing import Literal

from pydantic import Field

from augmentation.bootstrap.configuration.components.retriever_configuration import (
    RetrieverConfiguration,
    RetrieverName,
)


class BasicRetrieverConfiguration(RetrieverConfiguration):
    name: Literal[RetrieverName.BASIC] = Field(
        ..., description="The name of the retriever."
    )
