#!/usr/bin/env python3

from pathlib import Path
from shutil import copy as cp

from src import get
from src.defaults import defaults
from src.load import frompath as load


def copy(
    data: Path,
    origin: Path,
    destination: Path,
    verbose: bool = defaults.VERBOSE,
) -> None:
    """
    Copy recursively the directories registered in a list, from one directory
    to another.

    The intended use is to copy the top albums (found in the ``wanted`` list)
    from a big music library to a more selective one.

    Parameters
    ----------
        data:
            Path to the JSON file, which contains a dictionary of album
            objects, each with at least the fields: artist, title, and year.
        origin:
            Path to the directory containing individual album directories,
            each representing an album from ``data`` objects.
        destination:
            Path where the directories from ``origin`` will be copied to.
        verbose:
            Show information about current processes.
    """
    if verbose:
        print(f"""
              Moving directories registered in {data.name}
              Origin: {origin}
              Destination: {destination}
              """)
    for d in load(data):
        path = get.path(d)
        if verbose:
            print(f"Moving {path}.")
        fromPath = Path(origin / path)
        toPath = Path(destination / path)
        cp(fromPath, toPath)
    if verbose:
        print("Process completed.")
