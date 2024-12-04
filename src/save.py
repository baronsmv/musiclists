#!/usr/bin/env python3

import polars as pl

from src.debug import logging
from src.defaults import defaults
from src.defaults.path import PATH_TYPE
from src.get import file


def pl_config(markdown: bool = False) -> pl.Config:
    return pl.Config(
        fmt_str_lengths=30,
        tbl_cell_numeric_alignment="RIGHT",
        tbl_formatting="MARKDOWN" if markdown else "NOTHING",
        tbl_hide_dataframe_shape=True,
        tbl_hide_column_data_types=True,
        tbl_rows=1000000000,
    )


def as_df(
    data: list[dict] | pl.DataFrame,
    field: str,
    path_type: PATH_TYPE,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> None:
    logger = logging.logger(as_df)
    if verbose:
        print(f"Writing DataFrame to {field} file.")
    df = data if isinstance(data, pl.DataFrame) else pl.DataFrame(data)
    if path_type == "download":
        duplicates = df.filter(df.select("id").is_duplicated())
        if not duplicates.is_empty():
            with pl_config():
                logger.warning(
                    "Duplicated ID in the DataFrame:\n"
                    + str(duplicates.select("id", "artist", "title", "year"))
                    + "\nConsider increasing KEY_LENGTH in defaults (current one: "
                    + str(defaults.KEY_LENGTH)
                    + ")."
                )
    df.serialize(file.path(field, path_type=path_type))
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
    with pl_config(markdown=markdown):
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
