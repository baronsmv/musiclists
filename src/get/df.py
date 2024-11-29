#!/usr/bin/env python3

import polars as pl


def contextualize(
    df: pl.DataFrame,
    num_filter: dict[str, tuple[int | float, int | float]] | None,
    sort_by: dict[str, bool] | None,
    select: tuple | list | None,
    rename: dict | None,
) -> pl.DataFrame:
    if num_filter:
        df = df.filter(
            (pl.col(k) >= v[0]) & (pl.col(k) <= v[1])
            for k, v in num_filter.items()
        )
    if sort_by:
        df = df.sort(sort_by.keys(), descending=tuple(sort_by.values()))
    if select:
        df = df.select(select)
    if rename:
        df = df.rename(rename)
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
