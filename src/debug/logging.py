import logging
from types import FunctionType
from typing import Callable

from src.defaults.path import LOG_PATH

logging.basicConfig(
    filename=LOG_PATH,
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
    encoding="utf-8",
    level=logging.DEBUG,
)


def logger(func: FunctionType | Callable):
    l = logging.getLogger(func.__module__ + "." + func.__name__)
    l.info(
        f"Initiating `{func.__name__}` process of {func.__module__} module."
    )
    return l
