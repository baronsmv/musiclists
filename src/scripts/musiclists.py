#!/usr/bin/env python3

from pathlib import Path

import src.decorators.decorators as de
from src import write, output, compare
from src.copy import copy as cp
from src.defaults.choice import COLUMN_CHOICES


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

    This function downloads albums data whose scores (based on user ratings)
    meet the criteria set by `min_score`.

    The albums are downloaded in order of their score, and the process will
    stop as soon as an album with a score lower than `min_score` is found.

    The function provides detailed logging if `verbose` is enabled, and
    additional debugging information if `debug` is turned on.
    """
    write.aoty(
        min_score=min_score,
        max_score=max_score,
        types=types,
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

    This function downloads albums data whose scores (based on user ratings)
    meet the criteria set by `min_score`.

    The albums are downloaded in order of their score, and the process will
    stop as soon as an album with a score lower than `min_score` is found.

    The function provides detailed logging if `verbose` is enabled, and
    additional debugging information if `debug` is turned on.
    """
    write.prog(
        min_score=min_score,
        max_score=max_score,
        types=types,
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

    This function combines top album data from all sources, dealing with
    duplicates by their ID, and saves the result in the specified `path` in
    `polars` format.

    If `re_download` is specified, the albums in it will be downloaded again,
    otherwise, existing data will be reused.

    If `dedup` is enabled, besides the standard deduplication by ID, any
    duplicate albums found between the two sources registered in `dedup-path`
    will be removed as well.

    The process stops once all albums from both sources are merged, and albums
    that meet the minimum score criteria are included.

    The function provides detailed logging if `verbose` is enabled, and
    additional debugging information if `debug` is turned on.
    """
    compare.merge(
        data_1=data_1,
        data_2=data_2,
        columns=columns,
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
    output.albums(
        field=data,
        num_filter={
            "user_score": (min_score, max_score),
            "user_ratings": (min_ratings, max_ratings),
        },
        select=COLUMN_CHOICES
        if "all" in columns
        else {k: COLUMN_CHOICES[k] for k in columns},
        markdown=markdown,
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
    output.tracks(
        field="aoty",
        num_filter={
            "track_score": (min_score, max_score),
            "track_ratings": (min_ratings, max_ratings),
            "user_score": (min_album_score, max_album_score),
        },
        markdown=markdown,
    )


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


cli = de.cli


if __name__ == "__main__":
    cli()
