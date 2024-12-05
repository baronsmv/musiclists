#!/usr/bin/env python3

from src import load
from src import save
from src.defaults import defaults
from src.get import df as get_df


def albums(
    field: str,
    num_filter: dict[str, tuple[int | None, int | None]]
    | None = defaults.ALBUM_NUM_FILTER,
    sort_by: dict[str, bool] | None = defaults.ALBUM_SORT_BY,
    select: dict | tuple | list | None = defaults.ALBUM_SELECT,
    markdown: bool = True,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    df = load.df(field)
    df = get_df.contextualize(df, num_filter, sort_by, select)
    save.as_text(df, field + "_albums", markdown)


def tracks(
    field: str = "aoty",
    num_filter: dict[str, tuple[int | None, int | None]]
    | None = defaults.TRACKS_NUM_FILTER,
    sort_by: dict[str, bool] | None = defaults.TRACKS_SORT_BY,
    select: dict | tuple | list | None = defaults.TRACKS_SELECT,
    markdown: bool = True,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    df = load.df(field)
    df = get_df.tracks(df)
    df = get_df.contextualize(df, num_filter, sort_by, select)
    save.as_text(df, field + "_tracks", markdown)
