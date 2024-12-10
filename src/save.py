#!/usr/bin/env python3

import polars as pl


from src import load
from src.debug import logging
from src.defaults import defaults
from src.defaults.path import LOCATION
from src.get import file


def __pl_config__(markdown: bool = False) -> pl.Config:
    return pl.Config(
        fmt_str_lengths=30,
        tbl_cell_numeric_alignment="RIGHT",
        tbl_cols=-1,
        tbl_formatting="MARKDOWN" if markdown else "NOTHING",
        tbl_hide_dataframe_shape=True,
        tbl_hide_column_data_types=True,
        tbl_rows=1000000000,
        tbl_width_chars=300,
    )


def as_df(
    data: list[dict] | pl.DataFrame,
    name: str,
    location: LOCATION,
    append: bool = False,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> None:
    logger = logging.logger(as_df)
    name, exists = file.name_exists(name, location=location)
    if verbose:
        print(f"Writing DataFrame to {name} file.")
    df = data if isinstance(data, pl.DataFrame) else pl.DataFrame(data)
    if append and exists:
        col = df.columns
        df = (
            load.df(name, location=location)
            .select(col)
            .extend(df.select(col))
            .unique()
        )
    if location == "download":
        duplicates = df.filter(df.select("id").is_duplicated())
        if not duplicates.is_empty():
            with __pl_config__():
                logger.warning(
                    "Duplicated ID in the DataFrame:\n"
                    + str(duplicates.select("id", "artist", "album", "year"))
                    + "\nConsider increasing KEY_LENGTH in defaults (current one: "
                    + str(defaults.KEY_LENGTH)
                    + ")."
                )
    if debug:
        logger.debug(df)
    df.serialize(file.path(name, location=location))
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
    with __pl_config__(markdown=markdown):
        with open(
            file.path(
                field,
                suffix="md" if markdown else "txt",
                location="output",
            ),
            "w",
            encoding="utf-8",
        ) as f:
            f.write(str(df))
