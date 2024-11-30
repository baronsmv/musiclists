#!/usr/bin/env python3

from difflib import SequenceMatcher
from statistics import median

import polars as pl

from src.defaults import defaults


def diff(
    data1: pl.DataFrame,
    data2: pl.DataFrame,
    columns: list | tuple = ("title", "artist", "year"),
    minimum: int | float = 0.6,
    maximum: int | float = 1,
    only_highest_match: bool = defaults.ONLY_HIGHEST_MATCH,
    num_diff: float = 0.05,
):
    highest_ratio = 0.0
    highest_match = dict()
    for d1 in data1.rows(named=True):
        for d2 in data2.rows(named=True):
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
        if only_highest_match:
            yield highest_match
