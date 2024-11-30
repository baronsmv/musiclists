#!/usr/bin/env python3

from difflib import SequenceMatcher
from statistics import median

import polars as pl

from src import load
from src.get.album import path


def contextualize(
    df: pl.DataFrame,
    num_filter: dict[str, tuple[int | None, int | None]] | None,
    sort_by: dict[str, bool] | None,
    select: dict | tuple | list | None,
) -> pl.DataFrame:
    if num_filter:
        df = df.filter(
            (
                pl.col(k).is_between(
                    v[0] if v[0] else 0, v[1] if v[1] else 1000000000
                )
            )
            for k, v in num_filter.items()
        )
    if sort_by:
        df = df.sort(sort_by.keys(), descending=list(sort_by.values()))
    if select:
        if isinstance(select, dict):
            df = df.select(select.keys())
            df = df.rename(select)
        else:
            df = df.select(select)
    return df


def tracks(df: pl.DataFrame) -> pl.DataFrame:
    df = df.explode("tracks")
    df = pl.concat(
        [
            df,
            pl.json_normalize(
                df["tracks"],
                infer_schema_length=None,
            ),
        ],
        how="horizontal",
    )
    return df


def similarities(
    data_1: str,
    data_2: str,
    columns: list | tuple,
    minimum: int | float,
    maximum: int | float,
    only_highest_match: bool,
    num_diff: float,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    if not quiet:
        print(f"Finding similarities between {data_1} and {data_2}...")
    highest_ratio = 0.0
    highest_match = dict()
    for d1 in load.df(data_1).rows(named=True):
        for d2 in load.df(data_2).rows(named=True):
            # print(tuple((d1[col], d2[col]) for col in columns))
            # exit()
            match = median(
                (
                    SequenceMatcher(None, d1[col], d2[col]).ratio()
                    if isinstance(d1[col], str) or isinstance(d2[col], str)
                    else 1 - (abs(d1[col] - d2[col]) * num_diff)
                )
                for col in columns
            )
            if minimum <= match < maximum:
                if only_highest_match and match > highest_ratio:
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
