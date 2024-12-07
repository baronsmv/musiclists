#!/usr/bin/env python3

from src import load
from src import save
from src.defaults import defaults
from src.get import df


def duplicates(
    search,
    data_1: str,
    data_2: str,
    columns: list | tuple = ("album", "artist", "year"),
    min_rate: int | float = 0.6,
    only_highest_match: bool = defaults.ONLY_HIGHEST_MATCH,
    num_diff: float = 0.25,
    results: int = 15,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> None:
    data_search = dict()
    min_rate = 0 if search else min_rate
    name = f"{data_1}-{data_2}"
    if search:
        data_search = df.search(" ".join(search), data_1, columns, results)
        if not data_search:
            return
    matches = tuple(
        df.duplicates(
            data_1=data_1,
            data_2=data_2,
            search=data_search,
            dedup_name=name,
            columns=columns,
            min_rate=min_rate,
            results=results,
            only_highest_match=only_highest_match,
            num_diff=num_diff,
            quiet=quiet,
            verbose=verbose,
            debug=debug,
        )
    )
    if len(matches) == 0:
        if not quiet:
            print("Not found any new similarity.")
        return
    data = []
    for m in matches:
        data.append(
            dict(
                {
                    f"{c}-{d}": m[i][c]
                    for i, d in enumerate((data_1, data_2))
                    for c in ("id", "internal_id", "artist", "album", "year")
                }
            )
        )
    print(data)
    save.as_df(data, name, location="dedup", append=True)


def merge(
    data_1: str,
    data_2: str,
    columns: tuple,
    key: str = "id",
    dedup: bool = True,
    dedup_key: str = "internal_id",
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    name = f"{data_1}-{data_2}"
    data_2 = (
        df.deduplicated(data_2, data_1, key=dedup_key)
        if dedup
        else load.df(data_2)
    ).select(columns)
    data = (
        load.df(data_1)
        .select(columns)
        .join(data_2, on=columns, how="full", coalesce=True)
        .fill_null(strategy="zero")
        .unique(subset=key, keep="first")
    )
    print(data)
    save.as_df(data, name, location="merge")


def diff(
    data_1: str,
    data_2: str,
    columns: tuple,
    key: str = "id",
    dedup: bool = True,
    dedup_key: str = "internal_id",
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    name = f"{data_1}-{data_2}"
    d1 = (
        df.deduplicated(data_1, data_2, key=dedup_key)
        if dedup
        else load.df(data_1)
    ).select(columns)
    d2 = (
        df.deduplicated(data_2, data_1, key=dedup_key)
        if dedup
        else load.df(data_2)
    ).select(columns)
    data = d1.join(d2, on=key, how="anti")
    save.as_df(data, name, location="diff")
