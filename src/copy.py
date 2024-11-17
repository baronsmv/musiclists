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
            Path of the json file, which contains name/value pairs with
            objects with, at least, artist, title and year.
        origin:
            Directory that must store the albums corresponding to the data
            objects.
        destination:
            Directory the files will be copied to.
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
