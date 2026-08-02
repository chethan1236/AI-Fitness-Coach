"""Logging configuration shared by API and background processes."""

import logging
import sys

from app.core.config import settings


def configure_logging() -> None:
    """Configure a process-wide, human-readable console logger once."""
    root_logger = logging.getLogger()
    if root_logger.handlers:
        root_logger.setLevel(settings.log_level.upper())
        return

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    )
    root_logger.setLevel(settings.log_level.upper())
    root_logger.addHandler(handler)
