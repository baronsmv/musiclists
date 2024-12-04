#!/usr/bin/env python3

import pprint
from difflib import SequenceMatcher
from statistics import median
from typing import Iterator

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


def similarity(
    d1: dict | str,
    d2: dict,
    columns: list[str] | tuple[str],
    num_diff: float = 0,
) -> float:
    if isinstance(d1, str):
        return sum(
            SequenceMatcher(None, d1, str(d2[col])).ratio() for col in columns
        )
    return median(
        (
            SequenceMatcher(None, d1[col], str(d2[col])).ratio()
            if isinstance(d1[col], str)
            else 1 - (abs(d1[col] - d2[col]) * num_diff)
        )
        for col in columns
    )


def choice(
    matches: tuple | list,
    initial_prompt: str,
    side_by_side: str | None = None,
    choice_prompt: str = "Choose the desired option (0 to abort)",
    accept_prompt: str = "Accept the match?",
    final_prompt: str | None = None,
    any_to_abort: bool = False,
) -> dict | None:
    while True:
        if len(matches) > 1:
            i = input(
                f"\n{initial_prompt}:\n\n"
                + ("   " + side_by_side + "\n" if side_by_side else "")
                + "\n".join(
                    f"{n:4}) " + path(m, sep=" - ")
                    for n, m in enumerate(matches, start=1)
                )
                + f"\n\n{choice_prompt} [0-{len(matches)}]: "
            )
            if i.isdigit():
                i = int(i)
                if 0 < i <= len(matches):
                    match = matches[i - 1]
                    break
                elif i == 0:
                    return None
            elif not i and any_to_abort:
                return None
        else:
            i = input(
                f"\n{initial_prompt}:\n\n"
                + ("   " + side_by_side + "\n" if side_by_side else "")
                + f"   {path(matches[0])}"
                + f"\n\n{accept_prompt} [y/"
                + ("N" if any_to_abort else "n")
                + "]: "
            )
            if i.upper() == "Y":
                match = matches[0]
                break
            elif i.upper() == "N" or (not i and any_to_abort):
                return None
    if final_prompt:
        print(final_prompt)
    return match


def search(
    field: str,
    data: str,
    columns: list[str] | tuple[str],
    results: int,
) -> dict | None:
    return choice(
        tuple(
            r[1]
            for r in sorted(
                (
                    (similarity(field, d1, columns), d1)
                    for d1 in load.df(data).rows(named=True)
                ),
                key=lambda row: row[0],
                reverse=True,
            )[:results]
        ),
        f"Found similar refs. of «{field}» in «{data}»",
    )


def duplicates(
    data_1: str | dict,
    data_2: str,
    columns: list[str] | tuple[str],
    results: int,
    min_rate: int | float,
    only_highest_match: bool,
    num_diff: float,
    quiet: bool,
    verbose: bool,
    debug: bool,
) -> Iterator[tuple[dict, dict]]:
    logger = logging.logger(duplicates)
    data_1_str = data_1 if isinstance(data_1, str) else path(data_1, sep=" - ")
    start_message = (
        "Finding "
        + ("the highest match" if only_highest_match else "all matches")
        + f" between `{data_1_str}` and `{data_2}` data",
        f"in {columns}, and a minimum match rate of {min_rate * 100}%",
    )
    if debug:
        logger.info(" ".join(start_message))
    if not quiet:
        print((" ".join(start_message) if verbose else start_message[0]) + ".")
    rows_1 = (
        load.df(data_1).sort(by="id").rows(named=True)
        if isinstance(data_1, str)
        else (data_1,)
    )
    if debug:
        logger.info(f"Loaded {data_1_str} DataFrame rows into `data_1`.")
    rows_2 = load.df(data_2).rows(named=True)
    if debug:
        logger.info(f"Loaded {data_2} DataFrame rows into `data_2`.")
    for d1 in rows_1:
        matches = sorted(
            (
                (similarity(d1, d2, columns, num_diff), d1, d2)
                for d2 in rows_2
                if min_rate <= similarity(d1, d2, columns, num_diff)
            ),
            key=lambda row: row[0],
            reverse=True,
        )[:results]
        if not matches:
            if debug:
                logger.info("No matches found for: " + path(d1, sep=" - "))
            continue
        if (
            matches[0][0] != 1
            and max(
                similarity(matches[0][2], d, columns, num_diff) for d in rows_1
            )
            != 1
        ):
            if only_highest_match:
                match_message = (
                    f"Found match ({round(matches[0][0] * 100)}%) between",
                    path(matches[0][1], sep=" - "),
                    path(matches[0][2], sep=" - "),
                )
                c = choice(
                    (matches[0][2],),
                    match_message[0],
                    side_by_side=match_message[1],
                    final_prompt="Match accepted.",
                    any_to_abort=True,
                )
                if c:
                    yield matches[0][1:]
                    logger.info(
                        match_message[0] + ": " + ", ".join(match_message[1:])
                    )
                if debug:
                    logger.debug(pprint.pformat(matches[0]))
            else:
                match_message = (
                    "Found matches for",
                    path(matches[0][1], sep=" - "),
                )
                c = choice(
                    tuple(m[2] for m in matches),
                    match_message[0],
                    side_by_side=match_message[1],
                    choice_prompt="Choose the desired match (0 if no match if desired)",
                    final_prompt="Match accepted.",
                    any_to_abort=True,
                )
                if c:
                    yield matches[0][1], c
                    if debug:
                        logger.info(match_message + path(c, sep=" - "))
                if debug:
                    logger.debug(pprint.pformat(matches))
