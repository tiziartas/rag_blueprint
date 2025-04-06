from typing import AsyncIterator, Type

from core import Factory
from extraction.bootstrap.configuration.configuration import (
    ExtractionConfiguration,
)
from extraction.datasources.core.document import BaseDocument
from extraction.datasources.registry import DatasourceManagerRegistry
from extraction.orchestrators.base_orchestator import BaseDatasourceOrchestrator


class BasicDatasourceOrchestrator(BaseDatasourceOrchestrator):
    """Orchestrator for multi-datasource content processing.

    Manages extraction, embedding and storage of content from multiple
    datasources through a unified interface.

    Attributes:
        embedder: Component for generating embeddings
        datasources: Mapping of datasource type to manager
        documents: Raw documents from datasources
        cleaned_documents: Processed documents
        nodes: Text nodes for embedding
    """

    async def full_refresh_sync(self) -> AsyncIterator[BaseDocument]:
        """Extract and process content from all datasources.

        Processes each configured datasource to extract documents,
        clean content and generate text nodes.
        """
        for datasource_manager in self.datasource_managers:
            async for document in datasource_manager.full_refresh_sync():
                yield document

    async def incremental_sync(self) -> AsyncIterator[BaseDocument]:
        raise NotImplementedError("Incremental sync is not supported yet.")


class BasicDatasourceOrchestratorFactory(Factory):
    _configuration_class: Type = ExtractionConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: ExtractionConfiguration
    ) -> BasicDatasourceOrchestrator:
        """Creates a configured PDF reader.

        Args:
            configuration: Settings for PDF processing

        Returns:
            PDFDatasourceReader: Configured reader instance
        """
        datasource_managers = [
            DatasourceManagerRegistry.get(datasource_configuration.name).create(
                datasource_configuration
            )
            for datasource_configuration in configuration.extraction.datasources
        ]
        return BasicDatasourceOrchestrator(
            datasource_managers=datasource_managers
        )
