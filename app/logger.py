import logging
from functools import wraps
import sys

"""
НАСТРОЙКА ЛОГИРОВАНИЯ
"""


class LoggerFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    # format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    format = "%(levelname)s:%(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def debugging() -> bool:
    return hasattr(sys, 'gettrace') and sys.gettrace() is not None


def debuglog(debug: bool = False, message: str | None = None):
    def decorator(func: callable) -> callable:
        @wraps(func)
        def logging(*args, **kwargs):
            if debug:
                try:
                    log_msg = message if message else func.__name__
                    logger.debug(log_msg)
                    result = func(*args, **kwargs)
                    logger.debug(f"{log_msg} OK")
                    return result
                except Exception as e:
                    print(f"{func.__name__} interrupted with error {e}")
            else:
                return func(*args, **kwargs)
        return logging

    return decorator


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file = logging.FileHandler("testing.log")
file.setLevel(logging.INFO)
fileformat = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)")
# "%(asctime)s:%(levelname)s:%(message)s", datefmt="%H:%M:%S")
file.setFormatter(fileformat)
logger.addHandler(file)

stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
stream.setFormatter(LoggerFormatter())
logger.addHandler(stream)
