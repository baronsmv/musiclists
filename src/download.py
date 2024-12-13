#!/usr/bin/env python3

import multiprocessing.dummy as mp
from datetime import timedelta
from pathlib import Path
from textwrap import dedent

import mutagen

from src import dump
from src.attributes.local_dirs import album as album_attr, track as track_attr
from src.classes.Album import Album
from src.classes.MusicList import MusicList
from src.defaults import defaults
from src.defaults.download import (
    AOTY_TYPES,
    AOTY_MIN_SCORE,
    AOTY_MAX_SCORE,
    PROG_TYPES,
    PROG_MIN_SCORE,
    PROG_MAX_SCORE,
)
from src.get import data as get_data


def __download__(
    field: str,
    function,
    type1,
    type2,
    score_key: str,
    min_score: int | float,
    max_score: int | float,
    name: str | None = None,
    ceil: bool = defaults.CEIL,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    if verbose:
        print(
            dedent(
                f"""
            Download process started:
            - Types: {(
                    type1 if isinstance(type1, int) else
                    tuple(t[0] for t in type1)
                    if isinstance(type1[0], tuple)
                    else type1
                )}
            - Types: {(
                    type2 if isinstance(type2, int) else
                    tuple(t[0] for t in type2)
                    if isinstance(type2[0], tuple)
                    else type2
                )}
            - Minimum score: {min_score}
            - Maximum score: {max_score}
            """
            )
        )
    if not quiet:
        if name:
            print(f"Downloading lists from {name}:")
        else:
            print("Downloading lists:")
    data = (
        list()
    )  # type: list[dict[str, str | int | float | list | dict | timedelta]]
    until = dump.until(
        function=function,
        type1=type1,
        type2=type2,
        score_key=score_key,
        min_score=min_score,
        max_score=max_score,
        ceil=ceil,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )
    multithread = False
    if multithread:
        with mp.Pool(4) as executor:
            executor.map(data.append, until)
    else:
        for album in until:
            data.append(album)
    MusicList(data).save(f"download.{field}")


def aoty(
    field: str = "aoty",
    types: tuple = AOTY_TYPES,
    start_page: int = 1,
    min_score: int = AOTY_MIN_SCORE,
    max_score: int = AOTY_MAX_SCORE,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    __download__(
        field=field,
        function=dump.aoty,
        type1=types,
        type2=start_page,
        score_key="user_score",
        min_score=min_score,
        max_score=max_score,
        name="AOTY",
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )


def prog(
    field: str = "prog",
    types: tuple = tuple(PROG_TYPES.keys()),
    min_score: float = PROG_MIN_SCORE,
    max_score: float = PROG_MAX_SCORE,
    ceil: bool = defaults.CEIL,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    if not quiet:
        print("Generating list of genres...")
    __download__(
        field=field,
        function=dump.prog,
        type1=tuple(get_data.prog_genres().items()),
        type2=tuple((t, PROG_TYPES[t]) for t in types),
        score_key="user_score",
        min_score=min_score,
        max_score=max_score,
        name="Progarchives",
        ceil=ceil,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )


def dirs(
    source: Path,
    suffixes: tuple = ("opus", "mp3", "m4a", "flac"),
    album_data: dict = album_attr,
    track_data: dict = track_attr,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    albums = []
    album = Album()
    if not quiet:
        print(f"Registering music from '{source}'")
    for d in dump.dirs(source):
        print(d)
        track_files = tuple(
            mutagen.File(f) for s in suffixes for f in d.glob(f"*.{s}")
        )
        if len(track_files) == 0:
            continue
        print(track_files)
        album["id"] = ""
        for k, v in album_data.items():
            tag = track_files[0].get(v)
            print(d, k, v, tag)
            if not tag:
                continue
            album[k] = tag
        album["tracks"] = []
        for t in track_files:
            album["tracks"].append(
                {k: t[v] for k, v in track_data.items() if v in t}
            )
        album.compute_id()
        print(album)
        albums.append(album.copy())
        album.clear()
    print(albums)
    MusicList(albums).save("download.dirs")
