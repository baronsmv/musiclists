#!/usr/bin/env python3

import multiprocessing.dummy as mp
import json
from pathlib import Path
from pprint import pprint

from src.diff import diff
from src.dedup import dedup
from src import dump
from src import get
from src.load import frompath as load
from src import search

DEFAULT_VERBOSE = False

DEFAULT_AOTY_SCORE = 83
DEFAULT_PROG_SCORE = 3.95

DEFAULT_KEY_LENGTH = 14

DEFAULT_AUTO_FIELD = "possible"
DEFAULT_DEDUP_FIELD = "verified"
DEFAULT_SUFFIX = "json"


def totext(
    path: Path,
    textdir: Path,
    suffix: str = "txt",
    sep: str = " - ",
    sorted: bool = True
):
    txtPath = Path(Path(textdir) / f"{path.stem}.{suffix}")
    lines = [get.path(d, sep=sep) + "\n" for d in load(path).values()]
    if sorted:
        lines.sort()
    with open(txtPath, "w", encoding="utf-8") as f:
        f.writelines(lines)


def topath(
    path: Path,
    data: dict | set,
    textdir: Path,
    text: bool = False,
    verbose: bool = DEFAULT_VERBOSE
):
    if verbose:
        print(f"Saving list to {path}...")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    if text:
        totext(path=path, textdir=textdir)


def albums(
    path: Path,
    function,
    type1,
    type2,
    textdir: Path,
    lowerlimit: int | float,
    name: str | None = None,
    text: bool = False,
    verbose: bool = DEFAULT_VERBOSE,
):
    if verbose:
        print("Process started:")
        print(f"- {DEFAULT_SUFFIX.upper()} output: {path.absolute()}")
        if text:
            print(f"- TXT output: {textdir}/{path.stem}.txt")
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
    topath(path=path, data=data, textdir=textdir, text=text, verbose=verbose)
    if verbose:
        print("Process completed.")


def aoty(
    path: Path,
    textdir: Path,
    lowerlimit: int = DEFAULT_AOTY_SCORE,
    text: bool = False,
    verbose: bool = DEFAULT_VERBOSE,
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
        textdir=textdir,
        lowerlimit=lowerlimit,
        name="AOTY",
        text=text,
        verbose=verbose,
    )


def prog(
    path: Path,
    textdir: Path,
    lowerlimit: float = DEFAULT_PROG_SCORE,
    text: bool = False,
    verbose: bool = DEFAULT_VERBOSE,
):
    if verbose:
        print("Generating list of genres...")
    genres = tuple(i for i in dump.proggenres())
    albums(
        path=path,
        function=dump.progarchives,
        type1=genres,
        type2=(1),
        textdir=textdir,
        lowerlimit=lowerlimit,
        name="Progarchives",
        text=text,
        verbose=verbose,
    )


def dirs(
    musicdir: Path,
    dirspath: Path,
    textdir: Path,
    text: bool = False,
    verbose: bool = DEFAULT_VERBOSE,
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
    topath(
        path=dirspath,
        data=data,
        textdir=textdir,
        text=text,
        verbose=verbose,
    )


def all(
    path: Path,
    aotypath: Path,
    progpath: Path,
    dedupdir: Path,
    textdir: Path,
    dedup: bool = True,
    text: bool = False,
    verbose: bool = DEFAULT_VERBOSE,
):
    if verbose:
        print("Merging lists...")
    topath(
        path=path,
        data=dict(diff(
            data1=Path(aotypath),
            data2=Path(progpath),
            dedupdir=dedupdir,
            dedup=dedup),
        )
        | load(Path(progpath)),
        textdir=textdir,
        text=text,
        verbose=verbose,
    )


def duplicates(
    data1: Path,
    data2: Path,
    dedupdir: Path,
    textdir: Path,
    lowerlimit: int | float = 0.6,
    upperlimit: int | float = 1,
    field: str = DEFAULT_AUTO_FIELD,
    keysep: str = "-",
    keysuffix: str = DEFAULT_SUFFIX,
    text: bool = False,
    verbose: bool = DEFAULT_VERBOSE
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
    topath(path=path, data=data, textdir=textdir, text=text, verbose=verbose)


def differences(
    path: Path,
    data1: Path,
    data2: Path,
    name: str,
    dedupdir: Path,
    textdir: Path,
    suffix: str = DEFAULT_SUFFIX,
    dedup: bool = True,
    text: bool = True,
    verbose: bool = DEFAULT_VERBOSE,
) -> None:
    if verbose:
        print(f"Writting to {path.name}:")
    data = dict()
    for a1, a2 in diff(
        data1=data1, data2=data2, dedupdir=dedupdir, dedup=dedup
    ):
        data[a1] = a2
    topath(path=path, data=data, textdir=textdir, text=text, verbose=verbose)
