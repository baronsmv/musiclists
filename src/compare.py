#!/usr/bin/env python3

from difflib import SequenceMatcher
from statistics import median

from src import load
from src.defaults import defaults
from src.get.album import path


def diff(
    data_1: str,
    data_2: str,
    columns: list | tuple = ("title", "artist", "year"),
    minimum: int | float = 0.6,
    maximum: int | float = 1,
    only_highest_match: bool = defaults.ONLY_HIGHEST_MATCH,
    num_diff: float = 0.05,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    if not quiet:
        print(f"Finding similarities between {data_1} and {data_2}...")
    highest_ratio = 0.0
    highest_match = dict()
    for d1 in load.df(data_1).rows(named=True):
        for d2 in load.df(data_2).rows(named=True):
            sim = median(
                (
                    SequenceMatcher(None, d1[col], d2[col]).ratio()
                    if isinstance(d1[col], str)
                    else 1 - (abs(d1[col] - d2[col]) * num_diff)
                )
                for col in columns
            )
            if minimum <= sim < maximum:
                if only_highest_match and sim > highest_ratio:
                    highest_match = {d1: d2}
                elif not only_highest_match:
                    yield {d1: d2}
                    if verbose:
                        print(
                            f"- Found similarity between {path(d1)} and {path(d2)}."
                        )
        if only_highest_match and highest_match:
            yield highest_match
            if verbose:
                print(
                    f"- Found the highest similarity between "
                    + path(tuple(highest_match.items())[0])
                    + " and "
                    + path(tuple(highest_match.items())[1])
                    + "."
                )
            highest_ratio = 0.0
            highest_match.clear()
