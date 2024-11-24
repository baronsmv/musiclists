#!/usr/bin/env python3

from pathlib import Path

import src.decorators.decorators as de
from src import write
from src.copy import copy as cp


@de.aoty
def aoty(
    types: tuple,
    min_score: int,
    path: Path,
    text_path: Path,
    text: bool,
    verbose: bool,
    debug: bool,
):
    """
    Download a list of top albums from AlbumOfTheYear.org (AOTY).

    This function downloads albums data whose scores (based on user ratings)
    meet the criteria set by `min_score`, and saves them in the specified
    `path` in JSON format.

    Optionally, if `text` is enabled, the album data is also saved in a text
    format in the directory specified by `text_path`.

    The albums are downloaded in order of their score, and the process will
    stop as soon as an album with a score lower than `min_score` is found.

    The function provides detailed logging if `verbose` is enabled, and
    additional debugging information if `debug` is turned on.
    """
    write.aoty(
        path=path,
        text_path=text_path,
        min_score=min_score,
        types=types,
        text=text,
        verbose=verbose,
        debug=debug,
    )


@de.prog
def prog(
    types: tuple,
    min_score: float,
    path: Path,
    text_path: Path,
    text: bool,
    verbose: bool,
    debug: bool,
):
    """
    Download a list of top albums from ProgArchives.com.

    This function downloads albums data whose scores (based on user ratings)
    meet the criteria set by `min_score`, and saves them in the specified
    `path` in JSON format.

    Optionally, if `text` is enabled, the album data is also saved in a text
    format in the directory specified by `text_path`.

    The albums are downloaded in order of their score, and the process will
    stop as soon as an album with a score lower than `min_score` is found.

    The function provides detailed logging if `verbose` is enabled, and
    additional debugging information if `debug` is turned on.
    """
    write.prog(
        path=path,
        text_path=text_path,
        min_score=min_score,
        types=types,
        text=text,
        verbose=verbose,
        debug=debug,
    )


@de.merge
def merge(
    re_download: str,
    path: Path,
    text: bool,
    text_path: Path,
    dedup: bool,
    dedup_path: Path,
    aoty_min_score: int,
    prog_min_score: float,
    aoty_path: Path,
    prog_path: Path,
    verbose: bool,
    debug: bool,
):
    """
    Merge downloaded lists into one.

    This function combines top album data from all sources, dealing with
    duplicates by their ID, and saves the result in the specified `path` in
    JSON format.

    If `re_download` is specified, the albums in it will be downloaded again,
    otherwise, existing data will be reused.

    If `dedup` is enabled, besides the standard deduplication by ID, any
    duplicate albums found between the two sources registered in `dedup-path`
    will be removed as well.

    Optionally, if `text` is enabled, the album data is also saved in a text
    format in the directory specified by `text_path`.

    The process stops once all albums from both sources are merged, and albums
    that meet the minimum score criteria are included.

    The function provides detailed logging if `verbose` is enabled, and
    additional debugging information if `debug` is turned on.
    """
    if re_download == "all" or re_download == "aoty":
        write.aoty(
            path=aoty_path,
            min_score=aoty_min_score,
            text=False,
            verbose=verbose,
            debug=debug,
        )
        print()
    if re_download == "all" or re_download == "prog":
        write.prog(
            path=prog_path,
            min_score=prog_min_score,
            text=False,
            verbose=verbose,
            debug=debug,
        )
        print()
    write.all(
        path=path,
        text_path=text_path,
        aoty_path=aoty_path,
        prog_path=prog_path,
        dedup_path=dedup_path,
        dedup=dedup,
        text=text,
        verbose=verbose,
        debug=debug,
    )


@de.dirs
def dirs(
    source_path: Path,
    path: Path,
    text: bool,
    text_path: Path,
    verbose: bool,
    debug: bool,
):
    """
    Read album data from a directory and write it to a JSON file.

    This function scans the `source_path` directory, where albums are stored,
    and extracts their artist, name and year. The album data is then written
    to a JSON file in the `path` directory.

    Optionally, if `text` is enabled, the album data will also be saved in a
    text format in the directory specified by `text_path`.

    The function provides detailed logging if `verbose` is enabled, and
    additional debugging information if `debug` is turned on.
    """
    write.dirs(
        source=source_path,
        path=path,
        text_path=text_path,
        text=text,
        verbose=verbose,
        debug=debug,
    )


@de.wanted
def wanted(
    path: Path,
    text: bool,
    text_path: Path,
    dedup: bool,
    dedup_path: Path,
    merge_path: Path,
    dirs_path: Path,
    verbose: bool,
    debug: bool,
):
    """
    Identify the wanted but missing albums.

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

    Optionally, if `text` is enabled, the `wanted` albums will also be saved in
    text format in the directory specified by `text_path`.

    The function provides detailed logging if `verbose` is enabled, and
    additional debugging information if `debug` is turned on.
    """
    write.differences(
        path=path,
        text_path=text_path,
        data1=merge_path,
        data2=dirs_path,
        name="wanted",
        dedup=dedup,
        dedup_path=dedup_path,
        text=text,
        verbose=verbose,
        debug=debug,
    )


@de.leftover
def leftover(
    path: Path,
    text: bool,
    text_path: Path,
    dedup: bool,
    dedup_path: Path,
    dirs_path: Path,
    merge_path: Path,
    verbose: bool,
    debug: bool,
):
    """
    Identify the owned but unwanted albums.

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

    Optionally, if `text` is enabled, the `leftover` albums will also be saved
    in text format in the directory specified by `text_path`.

    The function provides detailed logging if `verbose` is enabled, and
    additional debugging information if `debug` is turned on.
    """
    write.differences(
        path=path,
        text_path=text_path,
        data1=dirs_path,
        data2=merge_path,
        name="left",
        dedup=dedup,
        dedup_path=dedup_path,
        text=text,
        verbose=verbose,
        debug=debug,
    )


@de.copy
def copy(
    source_path: Path,
    destination_path: Path,
    wanted_path: Path,
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
        verbose=verbose,
        debug=debug,
    )


cli = de.cli


if __name__ == "__main__":
    cli()
