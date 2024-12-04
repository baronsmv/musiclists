#!/usr/bin/env python3

from polars import col

from src import load
from src import save
from src.defaults import defaults
from src.get import df


def duplicates(
    search,
    data_1: str,
    data_2: str,
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
    dedup: bool = True,
    dedup_col: str = "internal_id",
):
    name = f"{data_1}_{data_2}"
    data = (
        load.df(data_1, path_type="download")
        .merge_sorted(load.df(data_2, path_type="download"), key="id")
        .unique(subset="id", keep="first")
    )
    if dedup:
        data_keys = data.select(dedup_col)
        col_1 = f"{data_1}_{dedup_col}"
        col_2 = f"{data_2}_{dedup_col}"
        dedup_dicts = (
            load.df(name, path_type="dedup").select(col_1, col_2).to_dicts()
        )
        data = data.filter(
            col(dedup_col)
            .is_in(k[col_2] for k in dedup_dicts if k[col_1] in data_keys)
            .not_()
        )
    save.as_df(data, name, path_type="merge")
