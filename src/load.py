#!/usr/bin/env python3

from polars import DataFrame

from src.defaults import defaults
from src.get import file


def df(
    field: str,
    dedup: bool = False,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> DataFrame:
    file_path = file.path(field, dedup=dedup)
    if verbose:
        print(f"Loading list from {file_path}...")
    return DataFrame.deserialize(file_path)
