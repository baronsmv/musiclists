#!/usr/bin/env python3

import multiprocessing.dummy as mp
import json
from pathlib import Path
from pprint import pprint

from src.diff import diff
from src.dedup import dedup
from src.defaults import defaults
from src import dump
from src import get
from src.load import frompath as load
from src import search


def to_text(
    path: Path,
    text_path: Path | None = None,
    suffix: str = "txt",
    sep: str = " - ",
    sorted: bool = True,
    verbose: bool = defaults.VERBOSE,
):
    if not text_path:
        return
    if verbose:
        print(f"Saving {defaults.TEXT_SUFFIX} list to {text_path}...")
    lines = [get.path(d, sep=sep) + "\n" for d in load(path).values()]
    if sorted:
        lines.sort()
    with open(text_path, "w", encoding="utf-8") as f:
        f.writelines(lines)


def to_path(
    path: Path,
    data: dict | set,
    text_path: Path | None = None,
    text: bool = False,
    verbose: bool = defaults.VERBOSE
):
    if verbose:
        print(f"Saving {defaults.SUFFIX} list to {path}...")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    if text:
        to_text(path=path, text_path=text_path, verbose=verbose)


def albums(
    path: Path,
    function,
    type1,
    type2,
    lowerlimit: int | float,
    text_path: Path | None = None,
    name: str | None = None,
    text: bool = False,
    verbose: bool = defaults.VERBOSE,
):
    if verbose:
        print("Process started:")
        print(f"- {defaults.SUFFIX.upper()} output: {path.absolute()}")
        if text and text_path:
            print(f"- TXT output: {text_path}")
        print("- Types: ", end="")
        pprint(type1)
        print("- Types: ", end="")
        pprint(type2)
        print(f"- Lower limit: {lowerlimit}")
        print()
        if name:
            print(f"Downloading lists from {name}:")
        else:
            print("Downloading lists:")
    data = dict()
    until = dump.until(
        function=function,
        type1=type1,
        type2=type2,
        lowerlimit=lowerlimit,
        verbose=verbose,
    )
    multithread = False
    if multithread:
        with mp.Pool(4) as executor:
            executor.map(data.update, until)
    else:
        for album in until:
            if (get.id(album)) in data:
                print(f"Elemento repetido:\n{album}")
                exit(1)
            data.update(album)
    to_path(
        path=path, data=data, text_path=text_path, text=text, verbose=verbose
    )
    if verbose:
        print("Process completed.")


def aoty(
    path: Path,
    text_path: Path | None = None,
    lowerlimit: int = defaults.AOTY_MIN_SCORE,
    text: bool = False,
    verbose: bool = defaults.VERBOSE,
):
    albums(
        path=path,
        function=dump.aoty,
        type1=(
            "LP",
            "EP",
            "Mixtape",
            "Compilation",
            "Live",
            "Soundtrack",
        ),
        type2=1,
        lowerlimit=lowerlimit,
        text_path=text_path,
        name="AOTY",
        text=text,
        verbose=verbose,
    )


def prog(
    path: Path,
    text_path: Path | None = None,
    lowerlimit: float = defaults.PROG_MIN_SCORE,
    text: bool = False,
    verbose: bool = defaults.VERBOSE,
):
    if verbose:
        print("Generating list of genres...")
    genres = tuple(i for i in dump.proggenres())
    albums(
        path=path,
        function=dump.progarchives,
        type1=genres,
        type2=(1),
        lowerlimit=lowerlimit,
        text_path=text_path,
        name="Progarchives",
        text=text,
        verbose=verbose,
    )


def dirs(
    musicdir: Path,
    dirspath: Path,
    text_path: Path | None = None,
    text: bool = False,
    verbose: bool = defaults.VERBOSE,
):
    data = dict()
    if verbose:
        print(f"Registering music from '{musicdir.name}'")
    for d in dump.dirs(musicdir):
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
        path=dirspath,
        data=data,
        text_path=text_path,
        text=text,
        verbose=verbose,
    )


def all(
    path: Path,
    aotypath: Path,
    progpath: Path,
    dedupdir: Path,
    text_path: Path | None = None,
    dedup: bool = True,
    text: bool = False,
    verbose: bool = defaults.VERBOSE,
):
    if verbose:
        print("Merging lists...")
    to_path(
        path=path,
        data=dict(diff(
            data1=Path(aotypath),
            data2=Path(progpath),
            dedupdir=dedupdir,
            dedup=dedup),
        )
        | load(Path(progpath)),
        text_path=text_path,
        text=text,
        verbose=verbose,
    )


def duplicates(
    data1: Path,
    data2: Path,
    dedupdir: Path,
    text_path: Path | None = None,
    lowerlimit: int | float = 0.6,
    upperlimit: int | float = 1,
    field: str = defaults.AUTO_FIELD,
    keysep: str = "-",
    keysuffix: str = defaults.SUFFIX,
    text: bool = False,
    verbose: bool = defaults.VERBOSE
) -> None:
    if verbose:
        print("Deduplicating lists...")
    path, data, inv = search.dedup(
        data1=data1,
        data2=data2,
        dedupdir=dedupdir,
        field=field,
        keysep=keysep,
        keysuffix=keysuffix,
    )
    for a1, a2 in dedup(
        load(data1), load(data2), lowerlimit, upperlimit
    ):
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
        path=path, data=data, text_path=text_path, text=text, verbose=verbose
    )


def differences(
    path: Path,
    data1: Path,
    data2: Path,
    name: str,
    dedupdir: Path,
    text_path: Path | None = None,
    suffix: str = defaults.SUFFIX,
    dedup: bool = True,
    text: bool = True,
    verbose: bool = defaults.VERBOSE,
) -> None:
    if verbose:
        print(f"Writting to {path}:")
    data = dict()
    for a1, a2 in diff(
        data1=data1, data2=data2, dedupdir=dedupdir, dedup=dedup
    ):
        data[a1] = a2
    to_path(
        path=path, data=data, text_path=text_path, text=text, verbose=verbose
    )
