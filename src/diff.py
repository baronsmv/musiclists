#!/usr/bin/env python3

from collections.abc import Iterator
from pathlib import Path

from src import get
from src.load import frompath as load
from src import search

DEFAULT_DEDUP = True
DEFAULT_VERIFIED_FIELD = "verified"


def diff(
    data1: Path,
    data2: Path,
    dedupdir: Path,
    field: str = DEFAULT_VERIFIED_FIELD,
    dedup: bool = DEFAULT_DEDUP,
) -> Iterator[tuple[str, dict]]:
    if not data1.exists() and not data2.exists():
        print("ERROR: Neither of list files exists, exiting...")
        exit(1)
    elif not data1.exists():
        for key, value in load(data2).values():
            yield key, value
    elif not data2.exists():
        for key, value in load(data1).values():
            yield key, value
    else:
        keys = load(data2).keys()
        data, inv = search.dedup(
            data1=data1, data2=data2, dedupdir=dedupdir
        )[1:]
        d = data[field]
        values = list()
        for k, v in d.items():
            if isinstance(v, list):
                for i in v:
                    values.append((k, i))
            else:
                values.append((k, v))
        for key, value in load(data1).items():
            if key not in keys:
                pt = get.path(value)
                if (
                    dedup
                    and not inv
                    and pt in d.keys()  # Exists as key in the dedup
                    and (
                        any(get.id(p) in keys for p in d[pt])
                        if isinstance(d[pt], list)
                        else get.id(d[pt]) in keys
                    )  # The value of the dedup exists in the second dict
                ):
                    continue
                elif (
                    dedup
                    and inv
                    and pt
                    in (v[1] for v in values)  # Exists as key in the dedup
                    and any(
                        (get.id(v[0]) in keys if pt == v[1] else False)
                        for v in values
                    )  # The value of the dedup exists in the second dict
                ):
                    continue
                else:
                    yield key, value
