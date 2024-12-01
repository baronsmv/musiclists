#!/usr/bin/env python3

import pprint
from difflib import SequenceMatcher
from statistics import median

import polars as pl

from src import load
from src.debug import logging
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


def __simil__(
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
    logger = logging.logger(similarities)
    start_message = (
        "Finding "
        + (
            "the highest similarities"
            if only_highest_match
            else "all similarities"
        )
        + f" between `{data_1}` and `{data_2}` data",
        f"in {columns}, and a minimum match rate of {minimum * 100}%",
    )
    logger.info(" ".join(start_message))
    if not quiet:
        print(
            (" ".join(start_message) if verbose else start_message[0]) + ".\n"
        )
    rows_1 = load.df(data_1).sort(by="id").rows(named=True)
    logger.info(f"Loaded {data_1} DataFrame rows into `data_1`.")
    rows_2 = load.df(data_2).sort(by="id").rows(named=True)
    logger.info(f"Loaded {data_2} DataFrame rows into `data_2`.")
    for d1 in rows_1:
        matches = sorted(
            (
                (__simil__(d1, d2, columns, num_diff), d1, d2)
                for d2 in rows_2
                if minimum <= __simil__(d1, d2, columns, num_diff)
            ),
            key=lambda row: row[0],
            reverse=True,
        )
        if not matches:
            logger.info("No matches found for: " + path(d1, sep=" - "))
            continue
        if (
            matches[0][0] != 1
            and max(
                __simil__(matches[0][2], d, columns, num_diff) for d in rows_1
            )
            != 1
        ):
            if only_highest_match:
                match_message = (
                    f"{round(matches[0][0] * 100)}%: Found match between:",
                    path(matches[0][1], sep=" - "),
                    path(matches[0][2], sep=" - "),
                )
                logger.info(
                    match_message[0] + " " + ", ".join(match_message[1:])
                )
                if debug:
                    logger.debug(pprint.pformat(matches[0]))
                if verbose:
                    print(*match_message, sep="\n- ")
                yield matches[0][1:]
            else:
                match_message = [
                    "Found matches for: "
                    + path(matches[0][1], sep=" - ")
                    + ":"
                ]
                for match in matches:
                    match_message.append(
                        f"{round(matches[0][0] * 100)}%: "
                        + path(match[2], sep=" - "),
                    )
                    yield match[1:]
                logger.info(
                    match_message[0] + ": " + ", ".join(match_message[1:])
                )
                if debug:
                    logger.debug(pprint.pformat(matches))
                if verbose:
                    print(*match_message, sep="\n- ")
