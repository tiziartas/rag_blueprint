import logging
import sys

from core.base_configuration import LogLevelName, MetadataConfiguration


class LoggerConfiguration:
    """Utility class for configuring application-wide logging.

    This class provides methods to create consistently configured loggers,
    manage log levels, and control the behavior of third-party loggers.
    It uses the log level settings from MetadataConfiguration by default.

    Attributes:
        LOG_FORMAT: The format string used for log messages
        log_level: The application-wide log level (cached from configuration)
    """

    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    log_level: LogLevelName = None

    @classmethod
    def get_logger(
        cls, name: str, log_level: LogLevelName = None, propagate: bool = False
    ) -> logging.Logger:
        """Create a logger with specified configuration.

        Args:
            name: Name for the logger (typically __name__)
            log_level: Logging level
            propagate: Whether to propagate to parent loggers

        Returns:
            logging.Logger: Configured logger instance
        """
        if not log_level:
            log_level = cls.get_log_level()

        logger = logging.getLogger(name)
        logger.setLevel(cls.log_level.value_as_int)
        logger.propagate = propagate

        if not logger.handlers:
            formatter = logging.Formatter(cls.LOG_FORMAT)
            handler = logging.StreamHandler(sys.stdout)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    @classmethod
    def get_log_level(cls) -> LogLevelName:
        """Get the log level for the logger.

        Returns:
            LogLevelName: The log level for the logger
        """
        if not cls.log_level:
            metadata = MetadataConfiguration()
            cls.log_level = metadata.log_level
        return cls.log_level

    @staticmethod
    def mute_logs():
        """Suppress verbose logs from third-party libraries.

        Sets appropriate log levels for various libraries to reduce log noise:
        - Sets 'httpx' to WARNING level
        - Sets 'pdfminer' to ERROR level
        """
        # Warning logs
        logging.getLogger("httpx").setLevel(logging.WARNING)

        # Error logs
        logging.getLogger("pdfminer").setLevel(logging.ERROR)


LoggerConfiguration.mute_logs()
