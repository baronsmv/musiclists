#!/usr/bin/env python3

import multiprocessing.dummy as mp
from pandas import DataFrame
from pathlib import Path
from textwrap import dedent

from src.diff import diff
from src.dedup import dedup
from src.defaults import defaults
from src import dump
from src import get
from src.html_tags import aoty as aoty_tags
from src.load import frompath as load
from src import search


def albums(
    path: Path,
    function,
    type1,
    type2,
    min_score: int | float,
    text_path: Path | None = None,
    name: str | None = None,
    text: bool = defaults.TEXT,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    if verbose:
        print(dedent(
            f"""
            Download process started:
            - Types: {type1}
            - Types: {type2}
            - Minimum score: {min_score}
            """))
        if name:
            print(f"Downloading lists from {name}:")
        else:
            print("Downloading lists:")
    data = list()  # type: list[dict[str, str | int | float | list]]
    until = dump.until(
        function=function,
        type1=type1,
        type2=type2,
        min_score=min_score,
        verbose=verbose,
        debug=debug,
    )
    multithread = True
    if multithread:
        with mp.Pool(4) as executor:
            executor.map(data.append, until)
    else:
        for album in until:
            data.append(album)
    DataFrame(data).to_feather(path)
    if verbose:
        print(f"{len(data)} albums registered.")


def aoty(
    path: Path,
    text_path: Path | None = None,
    types: tuple = defaults.AOTY_TYPES,
    start_page: int = 1,
    min_score: int = defaults.AOTY_MIN_SCORE,
    text: bool = defaults.TEXT,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    albums(
        path=path,
        function=dump.aoty,
        type1=defaults.AOTY_TYPES if "all" in types else types,
        type2=start_page,
        min_score=min_score,
        text_path=text_path,
        name="AOTY",
        text=text,
        verbose=verbose,
        debug=debug,
    )


def prog(
    path: Path,
    text_path: Path | None = None,
    types: tuple = defaults.PROG_TYPES,
    min_score: float = defaults.PROG_MIN_SCORE,
    text: bool = defaults.TEXT,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    if verbose:
        print("Generating list of genres...")
    genres = get.prog_genres()
    name_types = list()
    for i, t in enumerate(defaults.PROG_TYPES, start=1):
        if "all" in types or t in types:
            name_types.append(i)
    albums(
        path=path,
        function=dump.progarchives,
        type1=((k, v) for k, v in genres.items()),
        type2=name_types,
        min_score=min_score,
        text_path=text_path,
        name="Progarchives",
        text=text,
        verbose=verbose,
        debug=debug,
    )


def dirs(
    source: Path,
    path: Path,
    text_path: Path | None = None,
    text: bool = defaults.TEXT,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    data = dict()
    if verbose:
        print(f"Registering music from '{source.name}'")
    for d in dump.dirs(source):
        artist = d.parent.name.strip()
        if d.name[-5:-1].isdigit():
            year = d.name[-5:-1]
            title = d.name[:-7].strip()
        else:
            year = None
            title = d.name.replace(" ()", "").strip()
        album = {
            get.id((artist, year, title)): {
                "artist": artist,
                "title": title,
                "year": year,
            }
        }
        data.update(album)
    to_path(
        path=path,
        data=data,
        text_path=text_path,
        text=text,
        verbose=verbose,
        debug=debug,
    )


def all(
    path: Path,
    aoty_path: Path,
    prog_path: Path,
    dedup_path: Path,
    text_path: Path | None = None,
    dedup: bool = True,
    text: bool = defaults.TEXT,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    if verbose:
        print("Merging lists...")
    to_path(
        path=path,
        data=dict(
            diff(
                data1=Path(aoty_path),
                data2=Path(prog_path),
                dedup_path=dedup_path,
                dedup=dedup,
            ),
        )
        | load(Path(prog_path)),
        text_path=text_path,
        text=text,
        verbose=verbose,
        debug=debug,
    )


def duplicates(
    data1: Path,
    data2: Path,
    dedup_path: Path,
    text_path: Path | None = None,
    minimum: int | float = 0.6,
    maximum: int | float = 1,
    field: str = defaults.AUTO_FIELD,
    key_sep: str = "-",
    key_suf: str = defaults.SUFFIX,
    text: bool = defaults.TEXT,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> None:
    if verbose:
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
        verbose=verbose,
        debug=debug,
    )


def differences(
    path: Path,
    data1: Path,
    data2: Path,
    name: str,
    dedup_path: Path,
    text_path: Path | None = None,
    suffix: str = defaults.SUFFIX,
    dedup: bool = True,
    text: bool = True,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> None:
    if verbose:
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
        verbose=verbose,
        debug=debug,
    )
