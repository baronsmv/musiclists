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


@de.aoty
def aoty(
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


@de.prog
def prog(
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


@de.find
def find(
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
    ml_1 = MusicList().load(data_1)
    ml_2 = MusicList().load(data_2)
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


@de.union
def union(
    data_1: str,
    data_2: str,
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
    MusicList().load(data_1).union_with(
        other=MusicList().load(data_2),
        columns=tuple(ALBUM_COLUMNS.keys() if "all" in columns else columns),
        save=True,
        key=key,
        dedup=dedup,
        dedup_key=dedup_key,
    )


@de.intersect
def intersect(
    data_1: str,
    data_2: str,
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
    MusicList().load(data_1).intersect_with(
        other=MusicList().load(data_2),
        columns=tuple(ALBUM_COLUMNS.keys() if "all" in columns else columns),
        save=True,
        key=key,
    )


@de.diff
def diff(
    data_1: str,
    data_2: str,
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

    This function identifies the albums present in the first data list
    (`data_1`) but not in the second (`data_2`), selecting only the specified
    `columns` and using the given `key` to perform the comparison.

    If `dedup` is enabled, the function will remove any albums that appear in
    both lists (based on their `dedup_key`), in addition to calculating the
    difference between the two lists using the specified `key`.
    """
    MusicList().load(data_1).diff_with(
        other=MusicList().load(data_2),
        columns=tuple(ALBUM_COLUMNS.keys() if "all" in columns else columns),
        save=True,
        key=key,
        dedup=dedup,
        dedup_key=dedup_key,
    )


@de.albums
def albums(
    data: str,
    markdown: bool,
    min_score: int | float,
    max_score: int | float,
    min_ratings: int,
    max_ratings: int,
    columns: tuple,
    sort_by: tuple,
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
    MusicList().load(data).contextualize(
        num_filter={
            "user_score": (min_score, max_score),
            "user_ratings": (min_ratings, max_ratings),
        },
        select_rename=(
            ALBUM_COLUMNS
            if "all" in columns
            else {k: ALBUM_COLUMNS[k] for k in columns}
        ),
        sort_by={k: ALBUM_SORT_BY[k] for k in sort_by},
    ).table(
        save=True,
        as_md=markdown,
        name_postfix="_albums",
    )


@de.tracks
def tracks(
    data: str,
    markdown: bool,
    min_score: int,
    max_score: int,
    min_album_score: int,
    max_album_score: int,
    min_ratings: int,
    max_ratings: int,
    columns: tuple,
    sort_by: tuple,
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
    MusicList().load(data).tracks().contextualize(
        num_filter={
            "track_score": (min_score, max_score),
            "user_score": (min_album_score, max_album_score),
            "track_ratings": (min_ratings, max_ratings),
        },
        select_rename=(
            TRACK_COLUMNS
            if "all" in columns
            else {k: TRACK_COLUMNS[k] for k in columns}
        ),
        sort_by={k: TRACK_SORT_BY[k] for k in sort_by},
    ).table(
        save=True,
        as_md=markdown,
        name_postfix="_tracks",
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


'''
@de.wanted
def wanted(
    path: Path,
    dedup: bool,
    dedup_path: Path,
    merge_path: Path,
    dirs_path: Path,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Find the wanted but missing albums.

    This function takes two lists of albums:

        `merge_path` generated by the `merge` function (which combines albums
        from multiple sources).

        `dirs_path` generated by the `dirs` function (which stores albums
        from a directory)

    It compares these lists to identify which albums are `wanted` — i.e., the
    albums that are in the `merge` list but are missing from the `dirs` list.
    The resulting `wanted` albums will be saved in the `path` directory.

    If `dedup` is enabled, any duplicate albums found between the two lists
    registered in `dedup-path` will be omitted.

    The function provides detailed logging if `verbose` is enabled, and
    additional debugging information if `debug` is turned on.
    """
    write.differences(
        path=path,
        data1=merge_path,
        data2=dirs_path,
        name="wanted",
        dedup=dedup,
        dedup_path=dedup_path,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )


@de.leftover
def leftover(
    path: Path,
    dedup: bool,
    dedup_path: Path,
    dirs_path: Path,
    merge_path: Path,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Find the owned but unwanted albums.

    This function takes two lists of albums:

        `dirs_path` generated by the `dirs` function (which stores albums
        from a directory)

        `merge_path` generated by the `merge` function (which combines albums
        from multiple sources).

    It compares these lists to identify which albums are `leftover` — i.e., the
    albums that are in the `dirs` list but are missing from the `merge` list.
    The resulting `leftover` albums will be saved in the `path` directory.

    If `dedup` is enabled, any duplicate albums found between the two lists
    registered in `dedup-path` will be omitted.

    The function provides detailed logging if `verbose` is enabled, and
    additional debugging information if `debug` is turned on.
    """
    write.differences(
        path=path,
        data1=dirs_path,
        data2=merge_path,
        name="left",
        dedup=dedup,
        dedup_path=dedup_path,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )


@de.copy
def copy(
    source_path: Path,
    destination_path: Path,
    wanted_path: Path,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Copy wanted albums.

    This function copies directories (representing albums) from the
    `source_path` directory to the `destination_path` directory.

    It only copies directories that are listed in the `wanted_path` list,
    ensuring that only the `wanted` albums are moved.

    The albums are copied one by one, and the function provides detailed
    output if `verbose` is enabled, with additional debugging information
    available if `debug` is turned on.
    """
    cp(
        source=source_path,
        destination=destination_path,
        data=wanted_path,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )
'''

if __name__ == "__main__":
    cli()
