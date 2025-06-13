"""Logger configuration module for the application.
It sets up logging to both a file and the console, capturing warnings
and ensuring proper cleanup of handlers on exit"""
from datetime import datetime
import logging
import os
import sys

from utils.helpers import get_resource_path

LOG_DIR = get_resource_path("resources/logs")
os.makedirs(LOG_DIR, exist_ok=True)

log_filename = datetime.now().strftime("session_%Y-%m-%d_%H-%M-%S.log")
log_path = os.path.join(LOG_DIR, log_filename)

def capture_warnings():
    logging.captureWarnings(True)

def setup_logger():
    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


logger = setup_logger()
capture_warnings()


def cleanup():
    """Close all handlers properly."""
    logger.info("Cleaning up logger handlers before exit.")
    handlers = logger.handlers[:]
    for handler in handlers:
        handler.flush()
        handler.close()
        logger.removeHandler(handler)
