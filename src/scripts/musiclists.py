#!/usr/bin/env python3

from pathlib import Path

import src.decorators.commands as de
from src import download
from src.classes.MusicList import MusicList
from src.decorators.decorators import cli
from src.defaults.choice import (
    ALBUM_COLUMNS,
    TRACK_COLUMNS,
    ALBUM_SORT_BY,
    TRACK_SORT_BY,
)
from src.defaults.download import AOTY_TYPES, PROG_TYPES
from src.files import from_dir


@de.download_aoty
def download_aoty(
    types: tuple,
    min_score: int,
    max_score: int,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Download a list of top albums from AlbumOfTheYear.org (AOTY).

    This function retrieves albums whose scores fall within the range defined by
    `min_score` and `max_score`. The albums are fetched starting from the one
    with a score closest to `max_score` and will stop once an album with a score
    below `min_score` is encountered.
    """
    download.aoty(
        min_score=min_score,
        max_score=max_score,
        types=AOTY_TYPES if "all" in types else types,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )


@de.download_prog
def download_prog(
    types: tuple,
    min_score: int,
    max_score: int,
    ceil: bool,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Download a list of top albums from ProgArchives.com.

    This function retrieves albums whose scores fall within the range defined by
    `min_score` and `max_score`. The albums are fetched starting from the one
    with a score closest to `max_score` and will stop once an album with a score
    below `min_score` is encountered.

    Note: To ensure compatibility with other lists, the QWR scores from
    ProgArchives, which are originally in a decimal format ranging from 0 to 5,
    are converted to integers and saved into `user_score`, with a range from 0
    to 100, with rounding based on the `ceil` parameter (rounding either up or
    down).
    """
    download.prog(
        min_score=min_score,
        max_score=max_score,
        types=tuple(PROG_TYPES.keys()) if "all" in types else types,
        ceil=ceil,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )


@de.dedup_find
def dedup_find(
    search: list,
    columns: tuple,
    data_1: str,
    data_2: str,
    highest: bool,
    min_rate: float,
    max_results: int,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Find duplicate entries between lists.

    This function compares two album data lists to identify duplicates,
    considering for the match the specified columns provided in `columns`.

    If `SEARCH` is not empty, the function will search for a specific entry
    within `data_1` and then for duplicates of that entry in `data_2`.
    Otherwise, it compares all entries in `data_1` against `data_2`.
    """
    ml_1 = MusicList().load(data_1, type_="albums")
    ml_2 = MusicList().load(data_2, type_="albums")
    if search:
        ml_1 = ml_1.search_album(
            " ".join(search), columns, max_results, in_list=True
        )
        if ml_1 is None:
            return
    ml_1.find_duplicates_with(
        ml_2,
        save=True,
        min_rate=0 if search else min_rate,
        only_highest_match=highest,
        max_results=max_results,
    )


@de.albums_filter
def albums_filter(
    data: str,
    name: str,
    min_score: int,
    max_score: int,
    min_ratings: int,
    max_ratings: int,
    columns: tuple,
    sort_by: tuple,
    limit_artist: int,
    limit_year: int,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Filter a list of albums.

    This function processes a list, filtering it based on album scores
    (`min_album_score`, `max_album_score`), ratings count (`min_ratings`,
    `max_ratings`), selected columns (`columns`).

    The resulting list is then sorted according to the parameters and saved.
    """
    MusicList().load(name=data, type_="albums").contextualize(
        num_filter={
            "user_score": (min_score, max_score),
            "user_ratings": (min_ratings, max_ratings),
        },
        sort_by={k: ALBUM_SORT_BY[k] for k in sort_by},
        limit_per={"year": limit_year, "artist": limit_artist},
        select_rename=(ALBUM_COLUMNS.keys() if "all" in columns else columns),
    ).save(name if name else data, location="filtered")


@de.tracks_filter
def tracks_filter(
    data: str,
    name: str,
    min_score: int,
    max_score: int,
    min_album_score: int,
    max_album_score: int,
    min_ratings: int,
    max_ratings: int,
    columns: tuple,
    sort_by: tuple,
    limit_album: int,
    limit_artist: int,
    limit_year: int,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Filter a list of tracks.

    This function processes a list, filtering it based on album scores
    (`min_album_score`, `max_album_score`), ratings count (`min_ratings`,
    `max_ratings`), selected columns (`columns`), and track scores (`min_score`,
    `max_score`).

    The resulting list is then sorted according to the parameters and saved.
    """
    MusicList().load(data, type_="tracks").contextualize(
        num_filter={
            "track_score": (min_score, max_score),
            "user_score": (min_album_score, max_album_score),
            "track_ratings": (min_ratings, max_ratings),
        },
        sort_by={k: TRACK_SORT_BY[k] for k in sort_by},
        limit_per={
            "year": limit_year,
            "artist": limit_artist,
            "id": limit_album,
        },
        select_rename=(TRACK_COLUMNS.keys() if "all" in columns else columns),
    ).save(name if name else data, location="filtered")


@de.albums_union
def albums_union(
    data_1: str,
    data_2: str,
    name: str,
    columns: tuple,
    key: str,
    dedup: bool,
    dedup_key: str,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Merge downloaded lists into one, returning any album of each.

    This function combines album data from two sources (`data_1` and `data_2`),
    selecting only the specified `columns` and joining the lists based on the
    given `key`.

    If `dedup` is enabled, the function will remove duplicates based on the
    specified `dedup_key`, in addition to performing the standard deduplication
    by `key`.
    """
    MusicList().load(data_1, type_="albums").union_with(
        other=MusicList().load(data_2, type_="albums"),
        columns=tuple(ALBUM_COLUMNS.keys() if "all" in columns else columns),
        save=True,
        name=name,
        key=key,
        dedup=dedup,
        dedup_key=dedup_key,
    )


@de.tracks_union
def tracks_union(
    data_1: str,
    data_2: str,
    name: str,
    columns: tuple,
    key: str,
    dedup: bool,
    dedup_key: str,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Merge downloaded lists into one, returning any album of each.

    This function combines album data from two sources (`data_1` and `data_2`),
    selecting only the specified `columns` and joining the lists based on the
    given `key`.

    If `dedup` is enabled, the function will remove duplicates based on the
    specified `dedup_key`, in addition to performing the standard deduplication
    by `key`.
    """
    MusicList().load(data_1, type_="tracks").union_with(
        other=MusicList().load(data_2, type_="tracks"),
        columns=tuple(TRACK_COLUMNS.keys() if "all" in columns else columns),
        save=True,
        name=name,
        key=key,
        dedup=dedup,
        dedup_key=dedup_key,
    )


@de.albums_intersect
def albums_intersect(
    data_1: str,
    data_2: str,
    name: str,
    columns: tuple,
    key: str,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Join lists, only returning albums that are in both lists.

    This function identifies the albums present in both data lists (`data_1`
    and `data_2`), selecting only the specified `columns` and using the given
    `key` to perform the comparison.
    """
    MusicList().load(data_1, type_="albums").intersect_with(
        other=MusicList().load(data_2, type_="albums"),
        columns=tuple(ALBUM_COLUMNS.keys() if "all" in columns else columns),
        save=True,
        name=name,
        key=key,
    )


@de.tracks_intersect
def tracks_intersect(
    data_1: str,
    data_2: str,
    name: str,
    columns: tuple,
    key: str,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Join lists, only returning tracks that are in both lists.

    This function identifies the tracks present in both data lists (`data_1`
    and `data_2`), selecting only the specified `columns` and using the given
    `key` to perform the comparison.
    """
    MusicList().load(data_1, type_="tracks").intersect_with(
        other=MusicList().load(data_2, type_="tracks"),
        columns=tuple(TRACK_COLUMNS.keys() if "all" in columns else columns),
        save=True,
        name=name,
        key=key,
    )


@de.albums_diff
def albums_diff(
    data_1: str,
    data_2: str,
    name: str,
    columns: tuple,
    key: str,
    dedup: bool,
    dedup_key: str,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Find the difference between lists.

    This function identifies the entries present in the first data list
    (`data_1`) but not in the second (`data_2`), selecting only the specified
    `columns` and using the given `key` to perform the comparison.

    If `dedup` is enabled, the function will remove any entries that appear in
    both lists (based on their `dedup_key`), in addition to calculating the
    difference between the two lists using the specified `key`.
    """
    MusicList().load(data_1, type_="albums").diff_with(
        other=MusicList().load(data_2, type_="albums"),
        columns=tuple(ALBUM_COLUMNS.keys() if "all" in columns else columns),
        save=True,
        name=name,
        key=key,
        dedup=dedup,
        dedup_key=dedup_key,
    )


@de.tracks_diff
def tracks_diff(
    data_1: str,
    data_2: str,
    name: str,
    columns: tuple,
    key: str,
    dedup: bool,
    dedup_key: str,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Find the difference between lists.

    This function identifies the entries present in the first data list
    (`data_1`) but not in the second (`data_2`), selecting only the specified
    `columns` and using the given `key` to perform the comparison.

    If `dedup` is enabled, the function will remove any entries that appear in
    both lists (based on their `dedup_key`), in addition to calculating the
    difference between the two lists using the specified `key`.
    """
    MusicList().load(data_1, type_="tracks").diff_with(
        other=MusicList().load(data_2, type_="tracks"),
        columns=tuple(TRACK_COLUMNS.keys() if "all" in columns else columns),
        save=True,
        name=name,
        key=key,
        dedup=dedup,
        dedup_key=dedup_key,
    )


@de.export_albums
def export_albums(
    markdown: bool,
    data: str,
    name: str,
    min_score: int | float,
    max_score: int | float,
    min_ratings: int,
    max_ratings: int,
    columns: tuple,
    sort_by: tuple,
    limit_artist: int,
    limit_year: int,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Export a list of albums to a text file.

    This function processes an album data list (`data`), applying filters based
    on the specified score range (`min_score`, `max_score`), ratings range
    (`min_ratings`, `max_ratings`), and the selected columns (`columns`).

    The resulting list is then sorted and optionally formatted as Markdown
    before being exported to a text file.
    """
    MusicList().load(data, type_="albums").contextualize(
        num_filter={
            "user_score": (min_score, max_score),
            "user_ratings": (min_ratings, max_ratings),
        },
        sort_by={k: ALBUM_SORT_BY[k] for k in sort_by},
        limit_per={"year": limit_year, "artist": limit_artist},
        select_rename=(
            ALBUM_COLUMNS
            if "all" in columns
            else {k: ALBUM_COLUMNS[k] for k in columns}
        ),
    ).table(
        save=True,
        name=name if name else None,
        as_md=markdown,
    )


@de.export_tracks
def export_tracks(
    markdown: bool,
    data: str,
    name: str,
    min_score: int,
    max_score: int,
    min_album_score: int,
    max_album_score: int,
    min_ratings: int,
    max_ratings: int,
    columns: tuple,
    sort_by: tuple,
    limit_album: int,
    limit_artist: int,
    limit_year: int,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Export a list of tracks to a text file.

    This function processes a list of tracks, filtering based on track scores
    (`min_score`, `max_score`), album scores (`min_album_score`,
    `max_album_score`), ratings count (`min_ratings`, `max_ratings`), and the
    selected columns (`columns`).

    The resulting list is then sorted and optionally formatted as Markdown
    before being exported to a text file.
    """
    MusicList().load(data, type_="tracks").contextualize(
        num_filter={
            "track_score": (min_score, max_score),
            "user_score": (min_album_score, max_album_score),
            "track_ratings": (min_ratings, max_ratings),
        },
        sort_by={k: TRACK_SORT_BY[k] for k in sort_by},
        limit_per={
            "year": limit_year,
            "artist": limit_artist,
            "id": limit_album,
        },
        select_rename=(
            TRACK_COLUMNS
            if "all" in columns
            else {k: TRACK_COLUMNS[k] for k in columns}
        ),
    ).table(
        save=True,
        name=name if name else None,
        as_md=markdown,
    )


@de.get
def get(
    path: Path,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Find album data from a directory.

    This function scans the `PATH` directory, where albums are stored, and
    extracts their data.
    """
    from_dir(
        source=path,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )


if __name__ == "__main__":
    cli()
