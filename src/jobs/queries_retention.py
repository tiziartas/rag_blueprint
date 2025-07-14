from datetime import datetime, timedelta
from typing import Iterator, List, Type

import psycopg2
from joblib import Logger
from langfuse.client import Langfuse
from psycopg2 import sql

from augmentation.bootstrap.configuration.langfuse_configuration import (
    LangfuseConfiguration,
)
from augmentation.langfuse.client import LangfuseClientFactory
from core.base_factory import Factory
from core.logger import LoggerConfiguration


class LangfuseRenetionJob:
    """Langfuse V2 API does not support trace deletion, therefore we need to delete traces manually."""

    def __init__(
        self,
        configuration: LangfuseConfiguration,
        client: Langfuse,
        logger: Logger = LoggerConfiguration.get_logger(__name__),
    ):
        """
        Args:
            langfuse_client (Langfuse): The Langfuse client instance to interact with the Langfuse API.
            logger (Logger): Logger instance for logging messages.
        """
        self.configuration = configuration
        self.client = client
        self.logger = logger

    def run(self):
        retention_days = self.configuration.retention_job.retention_days
        cutoff_date = datetime.now() - timedelta(days=retention_days)
        ids = list(self._get_traces(cutoff_date))
        self.logger.info(
            f"Found {len(ids)} traces to delete older than {cutoff_date}."
        )
        self.delete_traces(ids)

    def _get_traces(self, cutoff_date: datetime) -> Iterator[int]:
        """
        Fetches traces from Langfuse that are older than the specified cutoff date.

        Args:
            cuttoff_date (datetime): The date before which traces will be fetched.

        Returns:
            Iterator: An iterator over the fetched traces.
        """
        limit = 100
        response = self.client.fetch_traces(
            to_timestamp=cutoff_date, limit=limit
        )
        total_pages = response.meta.total_pages
        for trace in response.data:
            yield trace.id

        for page in range(2, total_pages + 1):
            response = self.client.fetch_traces(
                to_timestamp=cutoff_date, page=page, limit=limit
            )
            for trace in response.data:
                yield trace.id

    def delete_traces(self, ids: List[int]) -> None:
        """
        Deletes traces with the specified IDs from Langfuse.

        Args:
            trace_ids (List[int]): A list of trace IDs to delete.
        """
        if not ids:
            self.logger.info("No traces to delete.")
            return

        connnection = self._get_pg_connection()

        try:
            self._delete_related_dataset_run_items(
                trace_ids=ids, connection=connnection
            )
            self._delete_related_dataset_items(
                trace_ids=ids, connection=connnection
            )
            self._delete_related_scores(trace_ids=ids, connection=connnection)
            self._delete_related_observations(
                trace_ids=ids, connection=connnection
            )
            self._delete_traces(trace_ids=ids, connection=connnection)
            self.logger.info(f"Deleted {len(ids)} traces.")
        except psycopg2.Error as e:
            self.logger.error(f"Failed to delete traces. Database error: {e}")
            connnection.rollback()
        finally:
            connnection.close()

    def _delete_related_dataset_items(
        self, trace_ids: List[int], connection
    ) -> None:
        """
        Deletes datasets related to the specified trace IDs.

        Args:
            ids (List[int]): A list of trace IDs for which related datasets will be deleted.
        """
        cursor = connection.cursor()

        query = sql.SQL("DELETE FROM dataset_items WHERE source_trace_id IN %s")
        cursor.execute(query, (tuple(trace_ids),))
        connection.commit()
        self.logger.debug(
            f"Deleted {cursor.rowcount} datasets related to traces."
        )

    def _delete_related_dataset_run_items(
        self, trace_ids: List[int], connection
    ) -> None:
        """
        Deletes dataset runs related to the specified trace IDs.

        Args:
            ids (List[int]): A list of trace IDs for which related dataset runs will be deleted.
        """
        cursor = connection.cursor()

        query = sql.SQL("DELETE FROM dataset_run_items WHERE trace_id IN %s")
        cursor.execute(query, (tuple(trace_ids),))
        connection.commit()
        self.logger.debug(
            f"Deleted {cursor.rowcount} dataset runs related to traces."
        )

    def _delete_related_scores(self, trace_ids: List[int], connection) -> None:
        """
        Deletes scores related to the specified trace IDs.

        Args:
            trace_ids (List[int]): A list of trace IDs for which related scores will be deleted.
        """
        cursor = connection.cursor()
        query = sql.SQL("DELETE FROM scores WHERE trace_id IN %s")
        cursor.execute(query, (tuple(trace_ids),))
        connection.commit()
        self.logger.debug(
            f"Deleted {cursor.rowcount} scores related to traces."
        )

    def _delete_related_observations(
        self, trace_ids: List[int], connection
    ) -> None:
        """
        Deletes observations (spans, generations, events) related to the specified trace IDs.
        """
        cursor = connection.cursor()
        query = sql.SQL("DELETE FROM observations WHERE trace_id IN %s")
        cursor.execute(query, (tuple(trace_ids),))
        connection.commit()
        self.logger.debug(
            f"Deleted {cursor.rowcount} observations related to traces."
        )

    def _delete_traces(self, trace_ids: List[int], connection) -> None:
        """
        Deletes traces with the specified IDs from Langfuse.

        Args:
            trace_ids (List[int]): A list of trace IDs to delete.
        """
        cursor = connection.cursor()
        query = sql.SQL("DELETE FROM traces WHERE id IN %s")
        cursor.execute(query, (tuple(trace_ids),))
        connection.commit()
        self.logger.debug(f"Deleted {len(trace_ids)} traces.")

    def _get_pg_connection(self):
        """
        Retrieves a PostgreSQL connection using the configuration.

        Returns:
            psycopg2.extensions.connection: A PostgreSQL connection object.
        """
        return psycopg2.connect(
            host=self.configuration.database.host,
            port=self.configuration.database.port,
            database=self.configuration.database.db,
            user=self.configuration.database.secrets.user.get_secret_value(),
            password=self.configuration.database.secrets.password.get_secret_value(),
        )


class LangfuseRenetionJobFactory(Factory):

    _configuration_class: Type = LangfuseConfiguration

    @classmethod
    def _create_instance(
        cls, configuration: LangfuseConfiguration
    ) -> LangfuseRenetionJob:
        """
        Create an instance of QueriesRetentionService using the provided configuration.

        Args:
            configuration (LangfuseConfiguration): The configuration object used to create the instance.

        Returns:
            QueriesRetentionService: A new instance of QueriesRetentionService.
        """
        langfuse_client = LangfuseClientFactory.create(
            configuration=configuration
        )
        return LangfuseRenetionJob(
            configuration=configuration, client=langfuse_client
        )
