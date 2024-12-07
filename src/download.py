#!/usr/bin/env python3

import multiprocessing.dummy as mp
from datetime import timedelta
from pathlib import Path
from textwrap import dedent

from src import dump, save
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
                    tuple(t[0] for t in type1)
                    if isinstance(type1[0], tuple)
                    else type1
                )}
            - Types: {(
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
    save.as_df(data, field, location="download")


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
    path: Path,
    use_exiftool: bool = True,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    """
    if not quiet:
        print(f"Registering music from '{source.name}'")
    album = dict()
    if use_exiftool:
        album_tags = {
            "album": "Album",
            "artist": "Albumartist",
            "total_tracks": "Totaltracks",
            "total_discs": "Totaldiscs",
            "directory": "Directory",
            "original_year": "Originalyear",
            "label": "Label",
            "catalog_number": "Catalognumber",
        }
        track_tags = {
            "disc_number": "Discnumber",
            "track_number": "TrackNumber",
            "title": "Title",
            "artist": "Artist",
            "file_size": "FileSize",
            "file_type": "FileType",
        }
        suffixes = ("*.opus", "*.mp3", "*.m4a", "*.flac")
        with ExifToolHelper(common_args=None) as et:
            for d in dump.dirs(source):
                track_files = tuple(d.glob(s) for s in suffixes)
                metadata = et.get_metadata(track_files[0])[0]
                for k, v in album_tags.items():
                    album[k] = metadata[v]
                album["tracks"] = [
                    {
                        k: et.get_metadata(t)[0][v]
                        for k, v in track_tags.items()
                    }
                    for t in track_files
                ]
                print(album)
                exit()
    else:
        data = list()
        album = dict()
        for d in dump.dirs(source):
            album["artist"] = d.parent.name.strip()
            if d.name[-5:-1].isdigit():
                album["year"] = d.name[-5:-1]
                album["title"] = d.name[:-7].strip()
            else:
                album["title"] = d.name.replace(" ()", "").strip()
        album["id"] = get_album.id(album)
        data.append(album.copy())
    DataFrame(data).serialize(path)
    if not quiet:
        print(f"\n{len(data)} albums registered.")
    """
