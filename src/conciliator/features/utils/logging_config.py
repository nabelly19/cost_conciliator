"""
Central logging configuration.

All modules should import get_logger() instead of configuring logging themselves.
"""

import logging
from typing import Optional

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Returns a configured logger instance.

    Parameters
    -
    name : Optional[str]
        Logger name (usually __name__)

    Returns
    -
    logging.Logger
    """

    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            fmt ="%(asctime)s | %(levelname)s | %(name)s | %(message)s" 
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)

    return logger