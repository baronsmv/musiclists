#!/usr/bin/env python3

import re
from unicodedata import normalize

from src.defaults import defaults


def id(
    data: list | dict | str,
    length: int = 16,
    sep: str = "",
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> str:
    if isinstance(data, str):
        res = re.search(r"(^.*)(?:\/)(.*) \((.*)\)", data)
        if res is not None:
            return id(list(res.groups()))
        else:
            print(f"ID not identified for {data}.")
            return str()
    if isinstance(data, dict):
        return id([data.get(i) for i in ("artist", "year", "album")])
    result = str()
    sep_length = len(sep)
    for d in data:
        if not d:
            continue
        d = str(d)
        for pattern in (r"[Tt]he ", r" EP", r".*: "):
            d = re.sub(pattern, "", d)
        d = str(normalize("NFKD", d).encode("ascii", "ignore"))[2:]
        d = re.sub(r"[^0-9a-zA-Z]+", "", d)
        d = d[:length].lower()
        result += sep + d
    return result[sep_length:]


def repr(
    data: dict,
    sep: str = " - ",
    include_year: bool = True,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> str:
    return (
        data.get("artist", "")
        + sep
        + data.get("album", "")
        + (
            " (" + str(data.get("year")) + ")"
            if include_year and "year" in data
            else ""
        )
    )
