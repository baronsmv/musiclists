#!/usr/bin/env python3

from collections.abc import Iterator
from pathlib import Path

import src.defaults.path
from src import load
from src import search
from src.defaults import defaults
from src.get import file


def diff(
    data1: str,
    data2: str,
    dedup_path: Path = src.defaults.path.DEDUP_DIR,
    field: str = defaults.VERIFIED_FIELD,
    dedup: bool = defaults.DEDUP,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator[tuple[str, dict]]:
    if not quiet:
        print(f"Starting diff process between {data1} and {data2}...")
    keys = load.df(data2).select("id").to_list()
    file_path, data, inv = search.dedup(data1=data1, data2=data2)
    if not data:
        print(f"Diff file {file_path} not found.")
        exit(1)
    d = data[field]
    values = list()
    for k, v in d.items():
        if isinstance(v, list):
            for i in v:
                values.append((k, i))
        else:
            values.append((k, v))
    for key, value in load.df(data1).items():
        if key not in keys:
            pt = file.path(value)
            if (
                dedup
                and not inv
                and pt in d.keys()  # Exists as key in the dedup
                and (
                    any(id(p) in keys for p in d[pt])
                    if isinstance(d[pt], list)
                    else id(d[pt]) in keys
                )  # The value of the dedup exists in the second dict
            ):
                continue
            elif (
                dedup
                and inv
                and pt in (v[1] for v in values)  # Exists as key in the dedup
                and any(
                    (id(v[0]) in keys if pt == v[1] else False) for v in values
                )  # The value of the dedup exists in the second dict
            ):
                continue
            else:
                yield key, value
