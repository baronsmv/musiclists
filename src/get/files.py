#!/usr/bin/env python3

from pathlib import Path

from src.defaults import defaults


def level(
    child: Path,
    parent: Path,
    lvl: int = 0,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> int:
    if child.parent.absolute() == parent.absolute():
        return lvl
    else:
        return level(child.parent, parent, lvl + 1)
