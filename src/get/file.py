#!/usr/bin/env python3

from pathlib import Path

from src.defaults.defaults import DATA_SUFFIX
from src.defaults.path import DIRS, LOCATION, VALID_LOCATION


def path(
    name: str,
    suffix: str | None = DATA_SUFFIX,
    location: LOCATION = "download",
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
