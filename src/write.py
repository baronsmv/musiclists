#!/usr/bin/env python3

import multiprocessing.dummy as mp
from datetime import timedelta
from pathlib import Path
from textwrap import dedent

import src.defaults.download
from src import dump, save
from src.defaults import defaults
from src.get import data as get_data


def __albums__(
    field: str,
    function,
    type1,
    type2,
    score_key: str,
    min_score: int | float,
    max_score: int | float,
    highest_score: int | float = 100,
    name: str | None = None,
    no_tracklist: bool = defaults.NO_TRACKLIST,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    if verbose:
        print(
            dedent(
                f"""
            Download process started:
            - Types: {type1}
            - Types: {type2}
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
        highest_score=highest_score,
        no_tracklist=no_tracklist,
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
    save.as_df(data, field)


def aoty(
    field: str = "aoty",
    types: tuple = src.defaults.download.AOTY_TYPES,
    start_page: int = 1,
    min_score: int = src.defaults.download.AOTY_MIN_SCORE,
    max_score: int = src.defaults.download.AOTY_MAX_SCORE,
    no_tracklist: bool = defaults.NO_TRACKLIST,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    __albums__(
        field=field,
        function=dump.aoty,
        type1=src.defaults.download.AOTY_TYPES if "all" in types else types,
        type2=start_page,
        score_key="user_score",
        min_score=min_score,
        max_score=max_score,
        name="AOTY",
        no_tracklist=no_tracklist,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )


def prog(
    field: str = "prog",
    types: tuple = src.defaults.download.PROG_TYPES,
    min_score: float = src.defaults.download.PROG_MIN_SCORE,
    max_score: float = src.defaults.download.PROG_MAX_SCORE,
    no_tracklist: bool = defaults.NO_TRACKLIST,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    if not quiet:
        print("Generating list of genres...")
    genres = get_data.prog_genres()
    name_types = list()
    for i, t in enumerate(src.defaults.download.PROG_TYPES, start=1):
        if "all" in types or t in types:
            name_types.append(i)
    __albums__(
        field=field,
        function=dump.progarchives,
        type1=(tuple((k, v) for k, v in genres.items())),
        type2=name_types,
        score_key="user_score",
        min_score=min_score,
        max_score=max_score,
        highest_score=5,
        name="Progarchives",
        no_tracklist=no_tracklist,
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


def all(
    path: Path,
    aoty_path: Path,
    prog_path: Path,
    dedup_path: Path,
    text_path: Path | None = None,
    dedup: bool = True,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    """
    if not quiet:
        print("Merging lists...")
    to_path(
        path=path,
        data=dict(
            diff(
                data1=Path(get.file.path("aoty")),
                data2=Path(get.file.path("prog")),
                dedup_path=dedup_path,
                dedup=dedup,
            ),
        )
        | load(Path(get.file.path("prog"))),
        text_path=text_path,
        text=text,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )
    """


def duplicates(
    data1: Path,
    data2: Path,
    dedup_path: Path,
    text_path: Path | None = None,
    minimum: int | float = 0.6,
    maximum: int | float = 1,
    field: str = defaults.AUTO_FIELD,
    key_sep: str = "-",
    key_suf: str = defaults.DATA_SUFFIX,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> None:
    """
    if not quiet:
        print("Deduplicating lists...")
    path, data, inv = search.dedup(
        data1=data1,
        data2=data2,
        dedup_path=dedup_path,
        field=field,
        key_sep=key_sep,
        key_suf=key_suf,
    )
    for a1, a2 in dedup(load(data1), load(data2), minimum, maximum):
        if inv:
            a1, a2 = a2, a1
        if a1 not in data[field]:
            data[field][a1] = a2
        elif isinstance(data[field][a1], str) and data[field][a1] != a2:
            data[field][a1] = [data[field][a1], a2]
        elif isinstance(data[field][a1], list) and a2 not in data[field][a1]:
            data[field][a1].append(a2)  # type: ignore
    for match in data[field]:
        if isinstance(match, list) and len(match) == 1:
            match = match[0]
    to_path(
        path=path,
        data=data,
        text_path=text_path,
        text=text,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )
    """


def differences(
    path: Path,
    data1: Path,
    data2: Path,
    name: str,
    dedup_path: Path,
    text_path: Path | None = None,
    suffix: str = defaults.DATA_SUFFIX,
    dedup: bool = True,
    text: bool = True,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> None:
    """
    if not quiet:
        print(f"Writting to {path}:")
    data = dict()
    for a1, a2 in diff(
        data1=data1, data2=data2, dedup_path=dedup_path, dedup=dedup
    ):
        data[a1] = a2
    to_path(
        path=path,
        data=data,
        text_path=text_path,
        text=text,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )
    """
