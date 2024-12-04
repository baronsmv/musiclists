#!/usr/bin/env python3

from pathlib import Path

from src.defaults.defaults import DATA_SUFFIX
from src.defaults.path import DIRS, PATH_TYPE, VALID_PATH_TYPE


def path(
    name: str,
    suffix: str | None = DATA_SUFFIX,
    path_type: PATH_TYPE = "download",
) -> Path:
    if path_type not in VALID_PATH_TYPE:
        raise ValueError(
            f"`path_type` parameter must be one of {VALID_PATH_TYPE}"
        )
    path_name = name + ("." + suffix if suffix else "")
    path_dir = DIRS[path_type]
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
