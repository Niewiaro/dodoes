import logging
from enum import StrEnum

LOG_FORMAT_DEFAULT = "%(asctime)s %(levelname)s:%(message)s"
LOG_FORMAT_DEBUG = "%(asctime)s %(levelname)s:%(message)s:%(pathname)s:%(funcName)s:%(lineno)d"


class LogLevels(StrEnum):
    info = "INFO"
    warn = "WARN"
    error = "ERROR"
    debug = "DEBUG"


def configure_logging(log_level: str = LogLevels.error, filename: str = None, filemode: str = "a") -> None:
    log_level = str(log_level).upper()
    log_levels = [level.value for level in LogLevels]

    kwargs = {"level": log_level}
    if log_level not in log_levels:
        kwargs["level"] = LogLevels.error

    kwargs["datefmt"] = "%Y-%m-%dT%H:%M:%S"

    if log_level == LogLevels.debug:
        kwargs["format"] = LOG_FORMAT_DEBUG
    else:
        kwargs["format"] = LOG_FORMAT_DEFAULT

    if filename:
        kwargs["filename"] = filename
        kwargs["filemode"] = filemode

    logging.basicConfig(**kwargs)
