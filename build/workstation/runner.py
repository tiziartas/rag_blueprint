import logging
import sys

sys.path.append("./src")

import argparse
import os
import socket
from datetime import datetime
from enum import Enum

from pydantic import Field
from python_on_whales import DockerClient
from python_on_whales.exceptions import DockerException

from augmentation.bootstrap.initializer import AugmentationPackageLoader
from core.base_configuration import MetadataConfiguration
from core.configuration_retrievers import (
    BaseConfigurationRetriever,
    ConfiguratioRetriverRegistry,
)
from embedding.vector_stores.pgvector.configuration import (
    PGVectorStoreConfiguration,
)
from evaluation.bootstrap.configuration.configuration import (
    EvaluationConfiguration,
)


class BuildMetadataConfiguration(MetadataConfiguration):
    init: bool = Field(
        False, description="If set, then the initialization will be run."
    )
    deploy: bool = Field(
        False, description="If set, then the deployment will be run."
    )
    log_file: str = Field(
        "build/workstation/logs/build.log",
        description="The name of the log file.",
    )

    @classmethod
    def _get_parser(cls):
        parser = super()._get_parser()
        mode_group = parser.add_mutually_exclusive_group(required=True)
        mode_group.add_argument(
            "--init", action="store_true", help="Run initialization"
        )
        mode_group.add_argument(
            "--deploy", action="store_true", help="Run deployment"
        )
        parser.add_argument(
            "--log-file",
            type=str,
            help="The file to log the deployment output",
        )
        return parser

    @classmethod
    def _get_data(cls, data: dict, args: argparse.Namespace) -> dict:
        data = super()._get_data(data, args)
        if args.init:
            data["init"] = True
        if args.deploy:
            data["deploy"] = True
        if args.log_file:
            data["log_file"] = args.log_file
        return data


class FileAndConsoleLogger(logging.Logger):
    """Custom logger that writes to both file and console with timestamps."""

    def __init__(self, name: str, filename: str, level: int = logging.INFO):
        """Initialize the logger with both file and console handlers.

        Args:
            name: Logger name
            filename: Path to log file
            level: Logging level (default: INFO)
        """
        super().__init__(name, level)

        # Create log directory if it doesn't exist
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        # Create formatters and handlers
        formatter = logging.Formatter(
            fmt="[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        # File handler
        file_handler = logging.FileHandler(filename, mode="a")
        file_handler.setFormatter(formatter)
        self.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)

        # Register the logger
        logging.getLogger("").addHandler(file_handler)
        logging.getLogger("").addHandler(console_handler)


class BuildInitializer:

    def __init__(self):

        self.metadata = BuildMetadataConfiguration()
        self.build_name = self.metadata.build_name
        self.environment = self.metadata.environment
        self.logger = FileAndConsoleLogger(
            name=__name__,
            filename=self.metadata.log_file,
            level=self.metadata.log_level.value_as_int,
        )
        self.init = self.metadata.init
        self.deploy = self.metadata.deploy

        AugmentationPackageLoader(logger=self.logger).load_packages()
        self.configuration_retriever = self._get_configuration_retriever()
        self.configuration = self.configuration_retriever.get()
        self._export_configuration()

    def get_configuration(self) -> EvaluationConfiguration:
        if not self.configuration:
            self.configuration = self.configuration_retriever.get()
        return self.configuration

    def should_run_initialization(self) -> bool:
        return self.init

    def should_run_deployment(self) -> bool:
        return self.deploy

    def _get_configuration_retriever(self) -> BaseConfigurationRetriever:
        configuration_retriever_class = ConfiguratioRetriverRegistry.get(
            on_prem=True
        )
        return configuration_retriever_class(
            configuration_class=EvaluationConfiguration,
            metadata=self.metadata,
        )

    def _export_configuration(self):
        """Export the port configuration.

        Export the port configuration to the environment variables.
        It is required for docker-compose, so it is able to use ports from the configuration.
        """
        vector_store_configuration = self.configuration.embedding.vector_store
        os.environ["RAG__VECTOR_STORE__PORT_REST"] = str(
            vector_store_configuration.port
        )
        if isinstance(vector_store_configuration, PGVectorStoreConfiguration):
            os.environ["RAG__VECTOR_STORE__DATABASE_NAME"] = str(
                vector_store_configuration.database_name
            )
            os.environ["RAG__VECTOR_STORE__USERNAME"] = str(
                vector_store_configuration.secrets.username.get_secret_value()
            )
            os.environ["RAG__VECTOR_STORE__PASSWORD"] = str(
                vector_store_configuration.secrets.password.get_secret_value()
            )

        langfuse_configuration = self.configuration.augmentation.langfuse
        os.environ["RAG__LANGFUSE__DATABASE__PORT"] = str(
            langfuse_configuration.database.port
        )
        os.environ["RAG__LANGFUSE__DATABASE__NAME"] = (
            langfuse_configuration.database.db
        )
        os.environ["RAG__LANGFUSE__DATABASE__USER"] = (
            langfuse_configuration.database.secrets.user.get_secret_value()
        )
        os.environ["RAG__LANGFUSE__DATABASE__PASSWORD"] = (
            langfuse_configuration.database.secrets.password.get_secret_value()
        )
        os.environ["RAG__LANGFUSE__PORT"] = str(langfuse_configuration.port)

        os.environ["RAG__CHAINLIT__PORT"] = str(
            self.configuration.augmentation.chainlit.port
        )


class CommandRunner:
    """Command runner for deployment and initialization.

    Runs commands for interacting with OS.

    Attributes:
        logger: Logger for the deployment
        build_name: The name of the build to deploy
        environment: Name of runtime environment
        docker_compose_filename: The file containing the docker-compose configuration
    """

    def __init__(
        self,
        logger: FileAndConsoleLogger,
        configuraiton: EvaluationConfiguration,
        secrets_filepath: str,
        docker_compose_filename: str,
    ):
        """Initialize the command runner.

        Args:
            logger: Logger for the deployment
            build_name: The name of the build to deploy
            environment: Name of runtime environment
            docker_compose_filename: The file containing the docker-compose configuration
        """
        self.logger = logger
        self.configuration = configuraiton
        self.docker_compose_filename = docker_compose_filename

        self.docker_client = DockerClient(
            compose_files=[docker_compose_filename],
            compose_env_files=[secrets_filepath],
        )

    def is_port_in_use(self, port: int) -> bool:
        """Check if the port is in use.

        Args:
            port: The port to check

        Returns:
            bool: True if the port is in use, False otherwise
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(("localhost", port)) == 0

    def run_docker_service(
        self,
        service_name: str,
        detached: bool = False,
        build: bool = True,
    ) -> int:
        """Run the docker service.

        Run indicated docker service from the composer. If flagged, the service is built before running.
        Use detached mode for services that shouldn't be awaited.

        Args:
            service_name: The name of the service to run
            detached: Whether to run the service in detached mode
            build: Whether to build the service before running

        Returns:
            int: The return code of the command
        """
        try:
            if build:
                self.logger.info(f"Building docker service: {service_name}")
                self.docker_client.compose.build(
                    services=[service_name],
                    build_args={
                        "BUILD_NAME": self.configuration.metadata.build_name,
                        "ENV": self.configuration.metadata.environment.value,
                    },
                )

            self.logger.info(f"Running docker service: {service_name}")
            self.docker_client.compose.up(
                services=[service_name],
                detach=detached,
                abort_on_container_exit=not detached,
            )
            return 0
        except DockerException as e:
            self.logger.error(
                f"Error running docker service: {service_name}. Error: {e}. Args: {e.args}"
            )
            return e.return_code

    def cleanup(self) -> int:
        """Clean up the Docker resources.

        Clean up all the Docker resources, including volumes.

        Returns:
            int: The return code of the command
        """
        self.logger.info("Cleaning up Docker resources")
        self.docker_client.system.prune(all=True, volumes=True)


class Deployment:
    """Deployment of the services.

    Deployment of the services using the Docker Compose.

    Attributes:
        command_runner: Command runner for the deployment
        logger: Logger for the deployment
    """

    class ServiceName(str, Enum):
        """Service names for the deployment.

        It has to correspond to the names in docker compose yaml file."""

        UNIT_TESTS = "unit-tests"
        EMBEDDING = "embed"
        CHAT = "chat"
        EVALUATION = "evaluate"

    def __init__(
        self, command_runner: CommandRunner, logger: FileAndConsoleLogger
    ):
        """Initialize the deployment.

        Args:
            command_runner: Command runner for the deployment
            logger: Logger for the deployment
        """
        self.command_runner = command_runner
        self.logger = logger

    def run(self) -> None:
        """Run the deployment.

        Run the deployment of the services using the Docker Compose.
        If the unit tests fail, the deployment is stopped.

        The services are run in the following order:
        - Unit tests
        - Embedding
        - Chat
        - Evaluation

        If the service is not detached, it is awaited and its logs are redirected to the log file.
        """
        return_code = self.command_runner.run_docker_service(
            Deployment.ServiceName.UNIT_TESTS.value
        )
        if return_code != 0:
            self.logger.info("Unit tests failed. Exiting deployment.")
            sys.exit(1)
        self.command_runner.run_docker_service(
            Deployment.ServiceName.EMBEDDING.value
        )
        self.command_runner.run_docker_service(
            Deployment.ServiceName.CHAT.value, detached=True
        )
        self.command_runner.run_docker_service(
            Deployment.ServiceName.EVALUATION.value
        )


class Initialization:
    """Initialization of the services.

    Initialization of the services using the Docker Compose.

    Attributes:
        command_runner: Command runner for the initialization
        logger: Logger for the initialization
    """

    class ServiceName(str, Enum):
        """Service names for the initialization.

        It has to correspond to the names in docker compose yaml file.
        For vector stores, it has to correspond to VectorStoreName."""

        LANGFUSE = "langfuse"
        LANGFUSE_DB = "langfuse-db"

    def __init__(
        self, command_runner: CommandRunner, logger: FileAndConsoleLogger
    ):
        """Initialize the initialization.

        Args:
            command_runner: Command runner for the initialization
            logger: Logger for the initialization
        """
        self.command_runner = command_runner
        self.logger = logger

    def run(self) -> None:
        """Run the initialization.

        Run the initialization of the services using the Docker Compose.

        The services are run in the following order:
        - Vector store
        - Langfuse database
        - Langfuse
        """
        self._init_vector_store()
        self._init_langfuse_database()
        self._init_langfuse()

    def _init_vector_store(self) -> None:
        """Initialize the vector store.

        Initialize the vector store service using the Docker Compose.
        If the ports are already in use, the initialization is skipped."""
        vector_store_configuration = (
            self.command_runner.configuration.embedding.vector_store
        )
        vector_store_port_rest = vector_store_configuration.port

        if self.command_runner.is_port_in_use(vector_store_port_rest):
            self.logger.info(
                f"REST port {vector_store_port_rest} is already in use. Skipping {vector_store_configuration.name.value} initialization."
            )
            return
        else:
            self.command_runner.run_docker_service(
                vector_store_configuration.name.value, detached=True
            )

    def _init_langfuse_database(self) -> None:
        """Initialize the langfuse database.

        Initialize the langfuse database service using the Docker Compose."""
        langfuse_configuration = (
            self.command_runner.configuration.augmentation.langfuse
        )
        langfuse_db_port = langfuse_configuration.database.port

        if self.command_runner.is_port_in_use(langfuse_db_port):
            self.logger.info(
                f"Port {langfuse_db_port} is already in use. Skipping langfuse database server initialization."
            )
            return
        else:
            self.command_runner.run_docker_service(
                Initialization.ServiceName.LANGFUSE_DB.value, detached=True
            )

    def _init_langfuse(self) -> None:
        """Initialize the langfuse.

        Initialize the langfuse service using the Docker Compose."""
        langfuse_configuration = (
            self.command_runner.configuration.augmentation.langfuse
        )
        langfuse_port = langfuse_configuration.port

        if self.command_runner.is_port_in_use(langfuse_port):
            self.logger.info(
                f"Port {langfuse_port} is already in use. Skipping langfuse initialization."
            )
            return
        else:
            self.command_runner.run_docker_service(
                Initialization.ServiceName.LANGFUSE.value, detached=True
            )


def initialize(
    logger: FileAndConsoleLogger, command_runner: CommandRunner
) -> None:
    """
    Initialize the services.

    Args:
        logger: Logger for the initialization
        command_runner: Command runner for the initialization
    """
    logger.info("Start base services initialization.")
    Initialization(command_runner=command_runner, logger=logger).run()
    logger.info("Base services initialization finished.")


def deploy(logger: FileAndConsoleLogger, command_runner: CommandRunner) -> None:
    """
    Deploy the services.

    Args:
        logger: Logger for the deployment
        command_runner: Command runner for the deployment
    Note:
        Returns 1 if the unit tests fail.
    """
    try:
        logger.info("Start deployment.")
        Deployment(command_runner=command_runner, logger=logger).run()
        logger.info(
            f"Deployment with build name {command_runner.configuration.metadata.build_name} finished."
        )
    finally:
        command_runner.cleanup()
        logger.info(
            f"Deployment with build name {command_runner.configuration.metadata.build_name} finished."
        )


def main():
    """Main function for the deployment.

    If `--init` flag is passed initialization of the base services is run.
    Otherwise, if `--deploy` flag is passed deployment of the services is run.
    """
    initializer = BuildInitializer()
    command_runner = CommandRunner(
        logger=initializer.logger,
        configuraiton=initializer.get_configuration(),
        secrets_filepath=initializer.configuration_retriever._get_secrets_filepath(),
        docker_compose_filename="build/workstation/docker/docker-compose.yml",
    )

    if initializer.should_run_initialization():
        initialize(initializer.logger, command_runner)
    if initializer.should_run_deployment():
        deploy(initializer.logger, command_runner)


if __name__ == "__main__":
    main()
