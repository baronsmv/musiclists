#!/usr/bin/env python3

import logging
from types import FunctionType
from typing import Callable

from src.defaults.path import LOG_PATH

loggers = {}


class ConsoleFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(levelname)s: %(message)s"

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def logger(func: FunctionType | Callable):
    global loggers

    if loggers.get(func):
        return loggers.get(func)

    else:
        l = logging.getLogger(func.__module__ + "." + func.__name__)

        l.setLevel(logging.DEBUG)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(ConsoleFormatter())

        file_handler = logging.FileHandler(
            LOG_PATH, mode="a", encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
        )
        file_handler.setFormatter(file_formatter)

        l.addHandler(console_handler)
        l.addHandler(file_handler)

        loggers[func] = l

        return l
