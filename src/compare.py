#!/usr/bin/env python3
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
    save.as_df(data, f"{data_1}_{data_2}", dedup=True)
