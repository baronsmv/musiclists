#!/usr/bin/env python3

from pathlib import Path

from src.debug import logging
from src.defaults.choice import ALL_CHOICE
from src.defaults.defaults import DATA_SUFFIX
from src.defaults.path import DIRS, VALID_LOCATION


def path(
    name: str,
    location: str,
    suffix: str | None = None,
) -> Path:
    path_name = name + "." + (suffix if suffix else DATA_SUFFIX)
    path_dir = DIRS[location]
    return Path(path_dir / path_name)


def level(
    child: Path,
    parent: Path,
    lvl: int = 1,
) -> int:
    if child.parent.absolute() == parent.absolute():
        return lvl
    else:
        return level(child.parent, parent, lvl + 1)


def contains_dirs(dir_path: Path):
    for c in dir_path.iterdir():
        if c.is_dir():
            return True
    return False


def source(
    name: str,
) -> tuple[str, str, bool]:
    logger = logging.logger(source)
    new_name = name.split(".")
    if len(new_name) == 1:
        new_name = new_name[0]
        location = "download"
        prefix = ""
    elif len(new_name) == 2:
        location, new_name = new_name
        if location not in VALID_LOCATION:
            raise ValueError(
                f"`{location}` parameter must be one of {VALID_LOCATION}"
            )
        prefix = f"{location}."
    else:
        logger.error(
            f"{name} is empty or has more than two fields separated by a dot."
        )
        exit(1)
    if f"{prefix}{new_name}" in ALL_CHOICE:
        return location, new_name, True
    if "-" in new_name:
        ord_name = "-".join(sorted(new_name.split("-")))
        return location, ord_name, f"{prefix}{ord_name}" in ALL_CHOICE
    return location, new_name, f"{prefix}{new_name}" in ALL_CHOICE
