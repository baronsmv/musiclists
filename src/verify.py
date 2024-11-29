#!/usr/bin/env python3

from pathlib import Path

from src.defaults import defaults


def verify(
    path: Path,
    dir: bool = False,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    if not path.exists():
        print(f"'{path}' no existe.")
        exit(1)
    if dir and not path.is_dir():
        print(f"'{path}' no es un directorio.")
        exit(1)


def containsdirs(path: Path):
    for c in path.iterdir():
        if c.is_dir():
            return True
    return False
