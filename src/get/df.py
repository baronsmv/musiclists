#!/usr/bin/env python3

import polars as pl


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
        df = df.sort(sort_by.keys(), descending=tuple(sort_by.values()))
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
