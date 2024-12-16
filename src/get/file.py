#!/usr/bin/env python3

from pathlib import Path

from src.debug import logging
from src.defaults.choice import ALL_ALBUMS, ALL_TRACKS
from src.defaults.defaults import DATA_SUFFIX
from src.defaults.path import (
    LOCATION,
    TYPE,
    ALBUMS_LOCATIONS,
    TRACKS_LOCATIONS,
    VALID_TYPES,
)


def __verify__(type_, location, logger) -> Path:
    if type_ not in VALID_TYPES:
        logger.error(f"Type `{type_}` must be one of these: {VALID_TYPES}")
        exit(1)
    loc = ALBUMS_LOCATIONS if type_ == "albums" else TRACKS_LOCATIONS
    location = f"{type_}-{location}"
    if location not in loc:
        logger.error(
            f"`{location}` location parameter must be one of these: "
            f"{tuple(loc.keys())}"
        )
        exit(1)
    return loc[location]


def path(
    name: str,
    type_: TYPE,
    location: LOCATION,
    suffix: str | None = None,
) -> Path:
    path_name = name + "." + (suffix if suffix else DATA_SUFFIX)
    path_dir = __verify__(type_, location, logging.logger(path))
    return path_dir / path_name


def source(
    name: str,
    type_: TYPE,
    location: LOCATION,
    order: bool = False,
) -> tuple[str, TYPE, LOCATION, bool]:
    __verify__(type_, location, logging.logger(source))
    postfix = f".{location}" if location != "download" else ""
    files = ALL_ALBUMS if type_ == "albums" else ALL_TRACKS
    if f"{name}{postfix}" in files:
        return name, type_, location, True
    if order and "-" in name:
        ord_name = "-".join(sorted(name.split("-")))
        return ord_name, type_, location, f"{ord_name}{postfix}" in files
    return name, type_, location, f"{name}{postfix}" in files


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
