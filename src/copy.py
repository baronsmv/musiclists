#!/usr/bin/env python3

from pathlib import Path
from shutil import copy as cp

from src import get
from src.load import frompath as load

DEFAULT_VERBOSE = False


def copy(
    destination: Path,
    origin: Path,
    data: Path,
    verbose: bool = DEFAULT_VERBOSE,
) -> None:
    if verbose:
        print(f"Moving files in {data.name}:")
    for d in load(data):
        if verbose:
            print(f"Moving {d}...")
        fromPath = Path(origin / get.path(d))
        toPath = Path(destination / get.path(d))
        cp(fromPath, toPath)
    if verbose:
        print("Operation completed.")
