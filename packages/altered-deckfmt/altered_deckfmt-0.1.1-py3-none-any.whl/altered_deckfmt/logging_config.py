import logging
from logging.config import dictConfig


def setup_logging(log_level=logging.DEBUG) -> None:
    """Set up logging configuration."""
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {"format": "[{asctime}][{levelname}] {message}", "style": "{"}
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": log_level,
        },
    }

    dictConfig(logging_config)
