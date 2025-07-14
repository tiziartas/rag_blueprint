from typing import Literal, Union

from pydantic import ConfigDict, Field, SecretStr

from core import BaseConfiguration, BaseConfigurationWithSecrets, BaseSecrets


class LangfuseDatabaseConfiguration(BaseConfigurationWithSecrets):
    """Configuration for connecting to the Langfuse PostgreSQL database.

    Contains all database connection parameters and credentials required for the Langfuse
    observation and analytics platform.
    """

    class Secrets(BaseSecrets):
        """Secret credentials for Langfuse database authentication.

        All fields are loaded from environment variables with the prefix RAG__LANGFUSE__DATABASE__.
        """

        model_config = ConfigDict(
            env_file_encoding="utf-8",
            env_prefix="RAG__LANGFUSE__DATABASE__",
            env_nested_delimiter="__",
            extra="ignore",
        )

        user: SecretStr = Field(
            ...,
            description="Username for authenticating with the Langfuse database server",
        )
        password: SecretStr = Field(
            ...,
            description="Password for authenticating with the Langfuse database server",
        )

    host: str = Field(
        "127.0.0.1",
        description="Hostname or IP address of the Langfuse database server",
    )
    port: int = Field(
        5432,
        description="TCP port number on which the Langfuse database server is listening",
    )
    db: str = Field(
        "langfuse",
        description="Name of the specific database to connect to on the Langfuse server",
    )
    secrets: Secrets = Field(
        None, description="Authentication credentials for the Langfuse database"
    )


class LangfuseDatasetConfiguration(BaseConfiguration):
    """Configuration for a single dataset in Langfuse.

    Defines properties of a dataset that will be created or used in the Langfuse platform.
    """

    name: str = Field(
        ...,
        description="Unique identifier for the dataset in the Langfuse server",
    )
    description: str = Field(
        ...,
        description="Human-readable explanation of the dataset's purpose and contents",
    )
    metadata: dict = Field(
        {},
        description="Additional structured information about the dataset as key-value pairs",
    )


class LangfuseDatasetsConfiguration(BaseConfiguration):
    """Configuration for all datasets used in the Langfuse platform.

    Contains definitions for specialized datasets used for different purposes.
    """

    feedback_dataset: LangfuseDatasetConfiguration = Field(
        LangfuseDatasetConfiguration(
            name="feedback-dataset",
            description="Dataset created out of positive feedbacks from the chatbot",
        ),
        description="Dataset for storing and analyzing user feedback collected from the chatbot interactions",
    )
    manual_dataset: LangfuseDatasetConfiguration = Field(
        LangfuseDatasetConfiguration(
            name="manual-dataset",
            description="Dataset created directly by the user indicating the query and the correct answer",
        ),
        description="Dataset for storing manually curated query-answer pairs for evaluation and training",
    )


class LangfuseRetentionJobConfiguration(BaseConfiguration):
    name: str = Field(
        "langfuse_traces_retention_job",
        description="Unique identifier for the Langfuse retention job",
    )
    crontab: str = Field(
        "0 0 * * *",
        description="Cron expression defining the schedule for running the Langfuse retention job",
    )
    retention_days: int = Field(
        30,
        description="Number of days to retain traces in the Langfuse platform before automatic deletion",
    )


class LangfuseConfiguration(BaseConfigurationWithSecrets):
    """Main configuration for the Langfuse integration.

    Contains all settings required to connect to and use the Langfuse platform,
    including server connection details, authentication, and dataset configurations.
    """

    class Secrets(BaseSecrets):
        """API authentication credentials for Langfuse.

        All fields are loaded from environment variables with the prefix RAG__LANGFUSE__.
        """

        model_config = ConfigDict(
            env_file_encoding="utf-8",
            env_prefix="RAG__LANGFUSE__",
            env_nested_delimiter="__",
            extra="ignore",
        )

        public_key: SecretStr = Field(
            ...,
            description="Public API key for authenticating with the Langfuse service",
        )
        secret_key: SecretStr = Field(
            ...,
            description="Secret API key for authenticating with the Langfuse service",
        )

    host: str = Field(
        "127.0.0.1", description="Hostname or IP address of the Langfuse server"
    )
    protocol: Union[Literal["http"], Literal["https"]] = Field(
        "http",
        description="Network protocol to use when connecting to the Langfuse server",
    )
    port: int = Field(
        3000,
        description="TCP port number on which the Langfuse server is listening",
    )
    database: LangfuseDatabaseConfiguration = Field(
        description="Database connection configuration for the Langfuse server",
        default_factory=LangfuseDatabaseConfiguration,
    )
    datasets: LangfuseDatasetsConfiguration = Field(
        description="Configuration for all datasets managed in the Langfuse platform",
        default_factory=LangfuseDatasetsConfiguration,
    )
    chainlit_tag_format: str = Field(
        "chainlit_message_id: {message_id}",
        description="Template string for generating tags that link Chainlit messages to Langfuse traces",
    )
    retention_job: LangfuseRetentionJobConfiguration = Field(
        description="Configuration for the Langfuse retention job that manages trace data lifecycle",
        default_factory=LangfuseRetentionJobConfiguration,
    )
    secrets: Secrets = Field(
        None,
        description="API authentication credentials for the Langfuse service",
    )

    @property
    def url(self) -> str:
        """Generate the complete URL for connecting to the Langfuse server.

        Returns:
            str: Fully formatted URL with protocol, host, and port
        """
        return f"{self.protocol}://{self.host}:{self.port}"
