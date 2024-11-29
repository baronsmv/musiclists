#!/usr/bin/env python3

import polars as pl

from src.defaults import defaults


def as_text(
    df: pl.DataFrame,
    field: str,
    markdown: bool = True,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    with pl.Config(
        fmt_str_lengths=30,
        tbl_cell_numeric_alignment="RIGHT",
        tbl_formatting="MARKDOWN" if markdown else "NOTHING",
        tbl_hide_dataframe_shape=True,
        tbl_hide_column_data_types=True,
        tbl_rows=1000000000,
    ):
        with open(
            defaults.PATH(
                field, suffix="md" if markdown else "txt",
                export=True,
            ),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(str(df))
