#!/usr/bin/env python3

from src.defaults import defaults

from src.get import df


def duplicates(
    search,
    data_1: str,
    data_2: str,
    columns: list | tuple = ("title", "artist", "year"),
    minimum: int | float = 0.6,
    only_highest_match: bool = defaults.ONLY_HIGHEST_MATCH,
    num_diff: float = 0.25,
    results: int = 15,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> None:
    if search:
        data_1 = df.search(" ".join(search), data_1, columns, results)
    if not data_1:
        return
    print()
    for s in df.duplicates(
        data_1=data_1,
        data_2=data_2,
        columns=columns,
        minimum=minimum if not search else 0,
        results=results,
        only_highest_match=only_highest_match,
        num_diff=num_diff,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    ):
        pass
