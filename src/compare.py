#!/usr/bin/env python3

from src.defaults import defaults

from src.get import df


def similarities(
    data_1: str,
    data_2: str,
    columns: list | tuple = ("title", "artist", "year"),
    minimum: int | float = 0.6,
    only_highest_match: bool = defaults.ONLY_HIGHEST_MATCH,
    num_diff: float = 0.25,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    for s in df.similarities(
        data_1=data_1,
        data_2=data_2,
        columns=columns,
        minimum=minimum,
        only_highest_match=only_highest_match,
        num_diff=num_diff,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    ):
        pass
