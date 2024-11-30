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


def __median__(
    d1: dict,
    d2: dict,
    columns: list[str] | tuple[str],
    num_diff: float,
) -> float:
    return median(
        (
            SequenceMatcher(None, d1[col], d2[col]).ratio()
            if isinstance(d1[col], str)
            else 1 - (abs(d1[col] - d2[col]) * num_diff)
        )
        for col in columns
    )


def similarities(
    data_1: str,
    data_2: str,
    columns: list[str] | tuple[str],
    minimum: int | float,
    only_highest_match: bool,
    num_diff: float,
    quiet: bool,
    verbose: bool,
    debug: bool,
) -> tuple[list, list]:
    if not quiet:
        print(f"Finding similarities between {data_1} and {data_2}...")
    data_1 = load.df(data_1).sort(by="id").rows(named=True)
    data_2 = load.df(data_2).sort(by="id").rows(named=True)
    for d1 in data_1:
        matches = sorted(
            ((__median__(d1, d2, columns, num_diff), d1, d2) for d2 in data_2),
            key=lambda row: row[0],
            reverse=True,
        )
        if (
            minimum <= matches[0][0] < 1
            and max(
                __median__(matches[0][2], d, columns, num_diff) for d in data_1
            )
            != 1
        ):
            if only_highest_match:
                yield matches[0][1:]
                if verbose:
                    print(
                        f"- {round(matches[0][0] * 100)}%: Highest similarity between:",
                        path(matches[0][1], sep=" - "),
                        path(matches[0][2], sep=" - "),
                        sep="\n  - ",
                    )
            else:
                print(f"- {matches[1]}:")
                for match in matches:
                    if minimum <= match[0] < 1:
                        yield match[1:]
                        if verbose:
                            print(
                                f"  - {round(matches[0][0] * 100)}%:",
                                path(match[2], sep=" - "),
                            )
