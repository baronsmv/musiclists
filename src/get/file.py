#!/usr/bin/env python3

from pathlib import Path

from src.defaults.choice import ALL_CHOICE
from src.defaults.defaults import DATA_SUFFIX
from src.defaults.path import DIRS, LOCATION, VALID_LOCATION


def name_exists(
    name: str,
    location: LOCATION,
) -> tuple[str, bool]:
    prefix = location + "-" if location != "download" else ""
    if "-" in name:
        names = [name, "-".join(name.split("-")[::-1])]
        names.sort()
        if (prefix + names[1]) in ALL_CHOICE:
            return names[1], True
        return names[0], (prefix + names[0]) in ALL_CHOICE
    return name, (prefix + name) in ALL_CHOICE


def path(
    name: str,
    location: LOCATION,
    suffix: str | None = DATA_SUFFIX,
) -> Path:
    if location not in VALID_LOCATION:
        raise ValueError(
            f"`path_type` parameter must be one of {VALID_LOCATION}"
        )
    path_name = name + ("." + suffix if suffix else "")
    path_dir = DIRS[location]
    return Path(path_dir / path_name)


def level(
    child: Path,
    parent: Path,
    lvl: int = 0,
) -> int:
    if child.parent.absolute() == parent.absolute():
        return lvl
    else:
        return level(child.parent, parent, lvl + 1)
