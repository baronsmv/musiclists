#!/usr/bin/env python3

from src import load
from src import save
from src.defaults import defaults
from src.defaults.path import LOCATION
from src.get import df


def duplicates(
    search,
    data_1: str,
    data_2: str,
    data_1_location: LOCATION,
    data_2_location: LOCATION,
    columns: list | tuple = ("title", "artist", "year"),
    min_rate: int | float = 0.6,
    only_highest_match: bool = defaults.ONLY_HIGHEST_MATCH,
    num_diff: float = 0.25,
    results: int = 15,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> None:
    data = []
    data_search = dict()
    if search:
        data_search = df.search(" ".join(search), data_1, columns, results)
        if not data_search:
            return
        print()
    for s in df.duplicates(
        data_1=data_search if search else data_1,
        data_2=data_2,
        data_1_location=data_1_location,
        data_2_location=data_2_location,
        columns=columns,
        min_rate=min_rate if not search else 0,
        results=results,
        only_highest_match=only_highest_match,
        num_diff=num_diff,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    ):
        print(s)
        data.append(
            dict(
                {
                    f"{c}_{d}": s[i][c]
                    for i, d in enumerate((data_1, data_2))
                    for c in ("internal_id", "artist", "title", "year")
                }
            )
        )
    save.as_df(data, f"{data_1}_{data_2}", path_type="dedup")


def merge(
    data_1: str,
    data_2: str,
    data_1_location: LOCATION,
    data_2_location: LOCATION,
    key: str = "id",
    dedup: bool = True,
    dedup_col: str = "internal_id",
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    name = f"{data_1}_{data_2}"
    data_1 = (
        df.deduplicated(
            data_1, data_2, data_1_location, data_2_location, key=dedup_col
        )
        if dedup
        else load.df(data_1, location=data_1_location)
    )
    data = data_1.merge_sorted(
        load.df(data_2, location="download"), key=key
    ).unique(subset=key, keep="first")
    save.as_df(data, name, path_type="merge")


def diff(
    data_1: str,
    data_2: str,
    data_1_location: LOCATION,
    data_2_location: LOCATION,
    key: str = "id",
    dedup: bool = True,
    dedup_col: str = "internal_id",
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    name = f"{data_1}_{data_2}"
    d1 = (
        df.deduplicated(
            data_1, data_2, data_1_location, data_2_location, key=dedup_col
        )
        if dedup
        else load.df(data_1, location=data_1_location)
    )
    d2 = (
        df.deduplicated(
            data_2, data_1, data_2_location, data_1_location, key=dedup_col
        )
        if dedup
        else load.df(data_2, location=data_2_location)
    )
    data = d1.join(d2, on=key, how="anti")
    save.as_df(data, name, path_type="diff")
