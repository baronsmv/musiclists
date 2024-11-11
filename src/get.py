#!/usr/bin/env python3

from pathlib import Path
import re
from unicodedata import normalize


def get(data: dict, key: str):
    if not data.get(key):
        if key in tuple(data.values())[0]:
            return tuple(data.values())[0][key]
        else:
            return str()
    else:
        return data.get(key)


def artist(data: dict) -> str:
    return get(data, "artist")


def title(data: dict) -> str:
    return get(data, "title")


def year(data: dict) -> int:
    return get(data, "year")


def score(data: dict) -> int | float:
    return get(data, "score")


def id(
    data: list | tuple | dict[str, str | int | list] | str,
    length: int = 14,
    sep: str = "",
) -> str:
    if isinstance(data, str):
        res = re.search(
            r"(?P<artist>^.*)\/(?P<title>.*) \((?P<year>.*)\)", data
        )
        return id(tuple(res.group(p) for p in ("artist", "year", "title")))
    elif isinstance(data, dict):
        return id((artist(data), year(data), title(data)))
    dataStr = str()
    sepL = len(sep)
    for d in data:
        if not d:
            continue
        d = str(d)
        for pattern in (r"[Tt]he ", r" EP", r".*: "):
            d = re.sub(pattern, "", d)
        d = str(normalize("NFKD", d).encode("ascii", "ignore"))[2:]
        d = re.sub(r"[^0-9a-zA-Z]+", "", d)
        d = d[:length].lower()
        dataStr += sep + d
    return dataStr[sepL:]


def path(
    data: dict[str, str | list | int | float],
    sep: str = "/",
    includeyear: bool = True,
) -> str:
    return (
        artist(data)
        + sep
        + title(data)
        + (f" ({year(data)})" if includeyear else "")
    )


def level(child: Path, parent: Path, lvl: int = 0) -> int:
    if child.parent.absolute() == parent.absolute():
        return lvl
    else:
        return level(child.parent, parent, lvl + 1)
