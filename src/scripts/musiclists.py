#!/usr/bin/env python3

from pathlib import Path

import src.decorators.decorators as de
from src import write
from src.copy import copy as cp


@de.new_list
@de.aoty
@de.count_time
def aoty(
    aoty_path: Path,
    aoty_lower: int,
    text: bool,
    text_dir: Path,
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
        lowerlimit=aoty_lower,
        text=text,
        textdir=text_dir,
        verbose=verbose,
    )


@de.new_list
@de.prog
@de.count_time
def prog(
    prog_path: Path,
    prog_lower: float,
    text: bool,
    text_dir: Path,
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
        lowerlimit=prog_lower,
        text=text,
        textdir=text_dir,
        verbose=verbose,
    )


@de.new_list
@de.re_download
@de.merge_path
@de.dedup
@de.aoty
@de.prog
@de.count_time
def merge(
    merge_path: Path,
    dedup: bool,
    dedup_dir: Path,
    re_download: str,
    aoty_path: Path,
    aoty_lower: int,
    prog_path: Path,
    prog_lower: float,
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
            lowerlimit=aoty_lower,
            text=text,
            textdir=text_dir,
            verbose=verbose,
        )
    if re_download == "all" or re_download == "prog":
        write.prog(
            path=prog_path,
            lowerlimit=prog_lower,
            text=text,
            textdir=text_dir,
            verbose=verbose,
        )
    write.all(
        path=merge_path,
        aotypath=aoty_path,
        progpath=prog_path,
        dedupdir=dedup_dir,
        textdir=text_dir,
        dedup=dedup,
        text=text,
        verbose=verbose,
    )


@de.new_list
@de.music_path
@de.dirs_path
@de.count_time
def dirs(music_path, dirs_path, text, text_dir, verbose):
    write.dirs(
        musicdir=music_path,
        dirspath=dirs_path,
        text=text,
        textdir=text_dir,
        verbose=verbose,
    )


@de.new_list
@de.wanted_path
@de.merge_path
@de.dirs_path
@de.dedup
@de.count_time
def wanted(
    wanted_path: Path,
    merge_path: Path,
    dirs_path: Path,
    dedup: bool,
    dedup_dir: Path,
    text: bool,
    text_dir: Path,
    verbose: bool,
):
    """
    """
    write.differences(
        path=wanted_path,
        data1=merge_path,
        data2=dirs_path,
        name="wanted",
        dedup=dedup,
        dedupdir=dedup_dir,
        text=text,
        textdir=text_dir,
        verbose=verbose,
    )


@de.new_list
@de.leftover_path
@de.dirs_path
@de.merge_path
@de.dedup
@de.count_time
def leftover(
    leftover_path: Path,
    merge_path: Path,
    dirs_path: Path,
    dedup: bool,
    dedup_dir: Path,
    text: bool,
    text_dir: Path,
    verbose: bool,
):
    """
    """
    write.differences(
        path=leftover_path,
        data1=dirs_path,
        data2=merge_path,
        name="left",
        dedup=dedup,
        dedupdir=dedup_dir,
        text=text,
        textdir=text_dir,
        verbose=verbose,
    )


@de.new_command
@de.music_path
@de.destination_path
@de.wanted_path
@de.count_time
def copy(
    music_path: Path,
    destination_path: Path,
    wanted_path: Path,
    dedup: bool,
    dedup_dir: Path,
    text: bool,
    text_dir: Path,
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
