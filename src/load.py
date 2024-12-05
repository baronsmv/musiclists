#!/usr/bin/env python3

from polars import DataFrame

from src.debug import logging
from src.defaults import defaults
from src.defaults.choice import ALL_CHOICE
from src.defaults.path import LOCATION
from src.get.file import name_exists


def df(
    name: str,
    location: LOCATION = "download",
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> DataFrame:
    logger = logging.logger(df)
    prefix = location + "-" if location != "download" else ""
    name, exists = name_exists(name, location)
    if not exists:
        logger.error(f"Couldn't find {name} file in {ALL_CHOICE.keys()}.")
        exit(1)
    file_path = ALL_CHOICE[prefix + name]
    if verbose:
        print(f"Loading list from {file_path}...")
    return DataFrame.deserialize(file_path)
