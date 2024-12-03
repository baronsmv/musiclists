#!/usr/bin/env python3

import polars as pl

from src.defaults import defaults
from src.get import file


def as_df(
    data: list[dict],
    field: str,
    dedup: bool = False,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> None:
    if verbose:
        print(f"Writing DataFrame to {field} file.")
    df = pl.DataFrame(data)
    print(df)
    df.serialize(file.path(field, dedup=dedup))
    if not quiet:
        print(f"\n{len(data)} albums registered.")


def as_text(
    df: pl.DataFrame,
    field: str,
    markdown: bool = True,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> None:
    with pl.Config(
        fmt_str_lengths=30,
        tbl_cell_numeric_alignment="RIGHT",
        tbl_formatting="MARKDOWN" if markdown else "NOTHING",
        tbl_hide_dataframe_shape=True,
        tbl_hide_column_data_types=True,
        tbl_rows=1000000000,
    ):
        with open(
            file.path(
                field,
                suffix="md" if markdown else "txt",
                output=True,
            ),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(str(df))
