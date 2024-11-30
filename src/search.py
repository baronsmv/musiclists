#!/usr/bin/env python3

from polars import DataFrame

from src.defaults import defaults
from src.get import file.path
from src import load


def dedup(
    data1: str,
    data2: str,
    key_sep: str = defaults.KEY_SEP,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> tuple[str, DataFrame, bool]:
    key = data1 + key_sep + data2
    invKey = data2 + key_sep + data1
    inv = False
    if file.path(key, dedup=True).exists():
        file_path = key
        data = load.df(file_path)
    elif file.path(invKey, dedup=True).exists():
        file_path = invKey
        data = load.df(file_path)
        inv = True
    else:
        file_path = key
        data = DataFrame()
    return file_path, data, inv
