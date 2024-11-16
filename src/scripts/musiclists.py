#!/usr/bin/env python3

from pathlib import Path

import src.decorators.decorators as de
from src import write
from src.copy import copy as cp


@de.new_command
@de.aoty
@de.count_time
def aoty(
    aoty_lower: int,
    aoty_path: Path,
    aoty_text_path: Path,
    text: bool,
    verbose: bool,
):
    """
    Downloads list with the top albums by users from albumoftheyear.org

    It saves them in a list in <AOTY-PATH> (in JSON format), and optionally in
    directory <TEXTDIR> (in TXT format) if the <TEXT> if enabled.

    It continues until a score lower than <LOWERLIMIT> is reached.
    """
    write.aoty(
        path=aoty_path,
        text_path=aoty_text_path,
        lowerlimit=aoty_lower,
        text=text,
        verbose=verbose,
    )


@de.new_command
@de.prog
@de.count_time
def prog(
    prog_lower: float,
    prog_path: Path,
    prog_text_path: Path,
    text: bool,
    verbose: bool,
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
        lowerlimit=prog_lower,
        text=text,
        verbose=verbose,
    )


@de.new_command
@de.merge
@de.dedup
@de.aoty
@de.prog
@de.count_time
def merge(
    re_download: str,
    merge_path: Path,
    merge_text_path: Path,
    dedup: bool,
    dedup_path: Path,
    aoty_lower: int,
    aoty_path: Path,
    aoty_text_path: Path,
    prog_lower: float,
    prog_path: Path,
    prog_text_path: Path,
    text: bool,
    text_dir: Path,
    verbose: bool,
):
    """
    Merges lists into one.
    """
    print("Merging lists...")
    print()
    if re_download == "all" or re_download == "aoty":
        write.aoty(
            path=aoty_path,
            text_path=aoty_text_path,
            lowerlimit=aoty_lower,
            text=text,
            verbose=verbose,
        )
    if re_download == "all" or re_download == "prog":
        write.prog(
            path=prog_path,
            text_path=prog_text_path,
            lowerlimit=prog_lower,
            text=text,
            verbose=verbose,
        )
    write.all(
        path=merge_path,
        text_path=merge_text_path,
        aotypath=aoty_path,
        progpath=prog_path,
        dedupdir=dedup_path,
        dedup=dedup,
        text=text,
        verbose=verbose,
    )


@de.new_command
@de.path.music
@de.dirs
@de.count_time
def dirs(music_path, dirs_path, text, dirs_text_path, verbose):
    write.dirs(
        musicdir=music_path,
        dirspath=dirs_path,
        text_path=dirs_text_path,
        text=text,
        verbose=verbose,
    )


@de.new_command
@de.wanted
@de.path.merge
@de.path.dirs
@de.dedup
@de.count_time
def wanted(
    wanted_path: Path,
    text: bool,
    wanted_text_path: Path,
    merge_path: Path,
    dirs_path: Path,
    dedup: bool,
    dedup_dir: Path,
    verbose: bool,
):
    """
    """
    write.differences(
        path=wanted_path,
        text_path=wanted_text_path,
        data1=merge_path,
        data2=dirs_path,
        name="wanted",
        dedup=dedup,
        dedupdir=dedup_dir,
        text=text,
        verbose=verbose,
    )


@de.new_command
@de.leftover
@de.path.dirs
@de.path.merge
@de.dedup
@de.count_time
def leftover(
    leftover_path: Path,
    leftover_text_path: Path,
    dirs_path: Path,
    merge_path: Path,
    dedup: bool,
    dedup_dir: Path,
    text: bool,
    verbose: bool,
):
    """
    """
    write.differences(
        path=leftover_path,
        text_path=leftover_text_path,
        data1=dirs_path,
        data2=merge_path,
        name="left",
        dedup=dedup,
        dedupdir=dedup_dir,
        text=text,
        verbose=verbose,
    )


@de.new_command
@de.path.music
@de.path.destination
@de.path.wanted
@de.count_time
def copy(
    music_path: Path,
    destination_path: Path,
    wanted_path: Path,
    verbose: bool,
):
    """
    """
    cp(
        origin=music_path,
        destination=destination_path,
        data=wanted_path,
        verbose=verbose,
    )


cli = de.cli


if __name__ == "__main__":
    cli()
