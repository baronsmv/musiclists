#!/usr/bin/env python3

from pathlib import Path
import polars as pl

from src.get import df as get_df
from src.load import from_path as load
from src.defaults import defaults


def as_text(
    df: pl.DataFrame,
    path: Path,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    with pl.Config(
        fmt_str_lengths=30,
        tbl_cell_numeric_alignment="RIGHT",
        tbl_formatting="MARKDOWN",
        tbl_hide_dataframe_shape=True,
        tbl_hide_column_data_types=True,
        tbl_rows=1000000000,
    ):
        with open(path, "w", encoding="utf-8") as f:
            f.write(str(df))


def albums(
    field: str,
    filter: str | None = None,
    sort_by: str | None = None,
    select: str | None = "tracks",
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    df = load(defaults.DATA_CHOICES[field])
    as_text(df, defaults.PATH(field, suffix="txt", export=True))


def tracks(
    field: str,
    num_filter: dict[str, tuple[int | float, int | float]] | None = {
        "track_score": (95, 100),
    },
    sort_by: dict[str, bool] | None = {
        "artist": False,
        "title": False,
        "track_score": True,
    },
    select: tuple | list | None = (
        "track_score",
        "track_ratings",
        "track_number",
        "track_title",
        "artist",
        "title",
        "year",
    ),
    rename: dict | None = {
        "track_score": "ts",
        "track_ratings": "tr",
        "track_number": "tn",
    },
    normalize: tuple | list | None = ("track_title", "artist", "title"),
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    df = load(defaults.DATA_CHOICES[field])
    df = get_df.tracks(df)
    df = get_df.contextualize(df, num_filter, sort_by, select, rename)
    as_text(df, defaults.PATH(field, suffix="txt", export=True))
