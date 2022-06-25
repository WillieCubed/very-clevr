import logging
import sys


LOGGING_FORMAT = "[%(levelname)s] %(message)s"
DEFAULT_LOGGING_LEVEL = logging.INFO

logger = logging.getLogger()

logger.setLevel(DEFAULT_LOGGING_LEVEL)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter(LOGGING_FORMAT)
handler.setFormatter(formatter)
logger.addHandler(handler)


def enable_verbose_logger():
    """Set the default logging level to log debug messages."""
    logger.setLevel(logging.DEBUG)
