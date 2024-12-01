#!/usr/bin/env python3

from pathlib import Path

import src.defaults.path
from src.defaults import defaults


def path(
    name: str,
    suffix: str | None = defaults.DATA_SUFFIX,
    output: bool = False,
    dedup: bool = False,
) -> Path:
    path = name + ("." + suffix if suffix else "")
    path_dir = (
        src.defaults.path.OUTPUT_DIR
        if output
        else src.defaults.path.DEDUP_DIR
        if dedup
        else src.defaults.path.DATA_DIR
    )
    return Path(path_dir / path)


def level(
    child: Path,
    parent: Path,
    lvl: int = 0,
) -> int:
    if child.parent.absolute() == parent.absolute():
        return lvl
    else:
        return level(child.parent, parent, lvl + 1)
