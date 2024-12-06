#!/usr/bin/env python3

import src.decorators.commands as de
from src import export, compare
from src.decorators.decorators import cli
from src.defaults.choice import COLUMN_CHOICES
from src.defaults.download import AOTY_TYPES, PROG_TYPES


@de.aoty
def aoty(
    types: tuple,
    min_score: int,
    max_score: int,
    no_tracklist: bool,
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
    write.aoty(
        min_score=min_score,
        max_score=max_score,
        types=AOTY_TYPES if "all" in types else types,
        no_tracklist=no_tracklist,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )


@de.prog
def prog(
    types: tuple,
    min_score: float,
    max_score: float,
    no_tracklist: bool,
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
    """
    write.prog(
        min_score=min_score,
        max_score=max_score,
        types=tuple(PROG_TYPES.keys()) if "all" in types else types,
        no_tracklist=no_tracklist,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )


@de.duplicates
def duplicates(
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
    compare.duplicates(
        search=search,
        data_1=data_1,
        data_2=data_2,
        only_highest_match=highest,
        columns=columns,
        min_rate=min_rate,
        results=max_results,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )


@de.merge
def merge(
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
    Merge downloaded lists into one.

    This function combines album data from two sources (`data_1` and `data_2`),
    selecting only the specified `columns` and joining the lists based on the
    given `key`.

    If `dedup` is enabled, the function will remove duplicates based on the
    specified `dedup_key`, in addition to performing the standard deduplication
    by `key`.
    """
    compare.merge(
        data_1=data_1,
        data_2=data_2,
        columns=COLUMN_CHOICES
        if "all" in columns
        else {k: COLUMN_CHOICES[k] for k in columns},
        key=key,
        dedup=dedup,
        dedup_key=dedup_key,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )


@de.merge
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
    compare.merge(
        data_1=data_1,
        data_2=data_2,
        columns=COLUMN_CHOICES
        if "all" in columns
        else {k: COLUMN_CHOICES[k] for k in columns},
        key=key,
        dedup=dedup,
        dedup_key=dedup_key,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
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
    export.albums(
        field=data,
        num_filter={
            "user_score": (min_score, max_score),
            "user_ratings": (min_ratings, max_ratings),
        },
        select=COLUMN_CHOICES
        if "all" in columns
        else {k: COLUMN_CHOICES[k] for k in columns},
        markdown=markdown,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )


@de.tracks
def tracks(
    markdown: bool,
    min_score: int,
    max_score: int,
    min_album_score: int,
    max_album_score: int,
    min_ratings: int,
    max_ratings: int,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Export a list of tracks to a text file.

    This function processes a list of tracks, filtering based on track scores
    (`min_score`, `max_score`),album scores (`min_album_score`,
    `max_album_score`), ratings count (`min_ratings`, `max_ratings`), and the
    selected columns (`columns`).

    The resulting list is then sorted and
    optionally formatted as Markdown before being exported to a text file.
    """
    export.tracks(
        field="aoty",
        num_filter={
            "track_score": (min_score, max_score),
            "track_ratings": (min_ratings, max_ratings),
            "user_score": (min_album_score, max_album_score),
        },
        markdown=markdown,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )


'''
@de.dirs
def dirs(
    source_path: Path,
    quiet: bool,
    verbose: bool,
    debug: bool,
):
    """
    Find album data from a directory.

    This function scans the `source_path` directory, where albums are stored,
    and extracts their artist, name and year. The album data is then written
    to a `polars` file in the `path` directory.

    The function provides detailed logging if `verbose` is enabled, and
    additional debugging information if `debug` is turned on.
    """
    write.dirs(
        source=source_path,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )


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
    registered in `dedup-path` will be ommited.

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
    registered in `dedup-path` will be ommited.

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
