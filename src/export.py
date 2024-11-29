#!/usr/bin/env python3

import polars as pl

from src.defaults import defaults
from src.get import df as get_df
from src import load
from src import save


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
        "artist": "Artist",
        "title": "Album",
        "year": "Year",
    },
    markdown: bool = True,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    df = load.df(defaults.DATA_CHOICES[field])
    df = get_df.contextualize(df, num_filter, sort_by, select)
    save.as_text(df, field + "_albums", markdown)


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
    df = load.df(defaults.DATA_CHOICES[field])
    df = get_df.tracks(df)
    df = get_df.contextualize(df, num_filter, sort_by, select)
    save.as_text(df, field + "_tracks", markdown)
