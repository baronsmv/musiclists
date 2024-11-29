#!/usr/bin/env python3

from pathlib import Path
import polars as pl

from src.get import df as get_df
from src.load import from_path as load
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


def albums(
    field: str,
    num_filter: dict[str, tuple[int | None, int | None]] | None = {
        "user_score": (95, 100),
    },
    sort_by: dict[str, bool] | None = {
        "artist": False,
        "title": False,
        "user_score": True,
    },
    select: dict | tuple | list | None = {
        "user_score": "SC",
        "user_ratings": "Rts.",
        "artist": "Artist",
        "title": "Album",
        "year": "Year",
    },
    markdown: bool = True,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    df = load(defaults.DATA_CHOICES[field])
    df = get_df.contextualize(df, num_filter, sort_by, select)
    as_text(df, field + "_albums", markdown)


def tracks(
    field: str = "aoty",
    num_filter: dict[str, tuple[int | None, int | None]] | None = {
        "track_score": (90, None),
        "track_ratings": (10, None),
        "user_score": (None, None),
    },
    sort_by: dict[str, bool] | None = {
        "artist": False,
        "title": False,
        "track_number": False,
    },
    select: dict | tuple | list | None = {
        "track_score": "SC",
        "track_ratings": "Rts.",
        "track_number": "No.",
        "track_title": "Track Title",
        "artist": "Artist",
        "title": "Album",
        "year": "Year",
    },
    markdown: bool = True,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    df = load(defaults.DATA_CHOICES[field])
    df = get_df.tracks(df)
    df = get_df.contextualize(df, num_filter, sort_by, select)
    as_text(df, field + "_tracks", markdown)
