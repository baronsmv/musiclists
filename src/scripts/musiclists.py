#!/usr/bin/env python3

from pathlib import Path

import src.decorators.decorators as de
from src import write
from src.copy import copy as cp


@de.aoty
def aoty(
    aoty_min_score: int,
    aoty_path: Path,
    aoty_text_path: Path,
    text: bool,
    verbose: bool,
    debug: bool,
):
    """
    Download a list of top albums from AlbumOfTheYear.org (AOTY) based on user
    ratings.

    The function downloads albums data whose scores meet the criteria set by
    `aoty_lower`, and saves them in the specified `aoty_path` in JSON format.

    The albums are downloaded in order of their score, and the process will
    stop as soon as an album with a score lower than `aoty_lower` is found.

    Optionally, if `text` is enabled, the album data is also saved in a text
    format in the directory specified by `aoty_text_path`.
    """
    write.aoty(
        path=aoty_path,
        text_path=aoty_text_path,
        lowerlimit=aoty_min_score,
        text=text,
        verbose=verbose,
        debug=debug,
    )


@de.prog
def prog(
    prog_min_score: float,
    prog_path: Path,
    prog_text_path: Path,
    text: bool,
    verbose: bool,
    debug: bool,
):
    """
    Downloads list with the top albums by users from progarchives.com

    It saves them in a list in <PROG-PATH> (in JSON format), and optionally in
    directory <TEXTDIR> (in TXT format) if the <TEXT> if enabled.

    It continues until a score lower than <LOWERLIMIT> is reached.
    """
    write.prog(
        path=prog_path,
        text_path=prog_text_path,
        lowerlimit=prog_min_score,
        text=text,
        verbose=verbose,
        debug=debug,
    )


@de.merge
def merge(
    re_download: str,
    dedup: bool,
    dedup_path: Path,
    merge_path: Path,
    text: bool,
    merge_text_path: Path,
    aoty_min_score: int,
    prog_min_score: float,
    aoty_path: Path,
    prog_path: Path,
    verbose: bool,
    debug: bool,
):
    """
    Merges lists into one.
    """
    if re_download == "all" or re_download == "aoty":
        write.aoty(
            path=aoty_path,
            lowerlimit=aoty_min_score,
            text=False,
            verbose=verbose,
            debug=debug,
        )
        print()
    if re_download == "all" or re_download == "prog":
        write.prog(
            path=prog_path,
            lowerlimit=prog_min_score,
            text=False,
            verbose=verbose,
            debug=debug,
        )
        print()
    write.all(
        path=merge_path,
        text_path=merge_text_path,
        aotypath=aoty_path,
        progpath=prog_path,
        dedupdir=dedup_path,
        dedup=dedup,
        text=text,
        verbose=verbose,
        debug=debug,
    )


@de.dirs
def dirs(
    music_path: Path,
    dirs_path: Path,
    text: bool,
    dirs_text_path: Path,
    verbose: bool,
    debug: bool,
):
    """ """
    write.dirs(
        musicdir=music_path,
        dirspath=dirs_path,
        text_path=dirs_text_path,
        text=text,
        verbose=verbose,
        debug=debug,
    )


@de.wanted
def wanted(
    dedup: bool,
    dedup_path: Path,
    wanted_path: Path,
    text: bool,
    wanted_text_path: Path,
    merge_path: Path,
    dirs_path: Path,
    verbose: bool,
    debug: bool,
):
    """ """
    write.differences(
        path=wanted_path,
        text_path=wanted_text_path,
        data1=merge_path,
        data2=dirs_path,
        name="wanted",
        dedup=dedup,
        dedupdir=dedup_path,
        text=text,
        verbose=verbose,
        debug=debug,
    )


@de.leftover
def leftover(
    dedup: bool,
    dedup_path: Path,
    leftover_path: Path,
    leftover_text_path: Path,
    dirs_path: Path,
    merge_path: Path,
    text: bool,
    verbose: bool,
    debug: bool,
):
    """ """
    write.differences(
        path=leftover_path,
        text_path=leftover_text_path,
        data1=dirs_path,
        data2=merge_path,
        name="left",
        dedup=dedup,
        dedupdir=dedup_path,
        text=text,
        verbose=verbose,
        debug=debug,
    )


@de.copy
def copy(
    music_path: Path,
    destination_path: Path,
    wanted_path: Path,
    verbose: bool,
    debug: bool,
):
    """ """
    cp(
        source=music_path,
        destination=destination_path,
        data=wanted_path,
        verbose=verbose,
        debug=debug,
    )


cli = de.cli


if __name__ == "__main__":
    cli()
