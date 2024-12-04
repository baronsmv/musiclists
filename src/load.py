#!/usr/bin/env python3

from polars import DataFrame

from src.defaults import defaults
from src.defaults.path import PATH_TYPE
from src.get import file


def df(
    field: str,
    path_type: PATH_TYPE,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> DataFrame:
    file_path = file.path(field, path_type=path_type)
    if verbose:
        print(f"Loading list from {file_path}...")
    return DataFrame.deserialize(file_path)
