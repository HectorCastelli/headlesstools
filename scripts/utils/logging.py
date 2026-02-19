import os
import logging


def setup_logging():
    """
    Configures standard logging to respect LOG_ENV
    """
    logging.basicConfig(
        level=os.getenv("LOG_LEVEL", "INFO"), format="%(levelname)s: %(message)s"
    )
