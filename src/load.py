#!/usr/bin/env python3

from polars import DataFrame
from pathlib import Path

from src.defaults import defaults


def df(
    path: Path,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> DataFrame:
    if not quiet:
        print(f"Loading list from {path}...")
    return DataFrame.deserialize(path)
