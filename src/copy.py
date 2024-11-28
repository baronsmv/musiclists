#!/usr/bin/env python3

from pathlib import Path
from shutil import copy as cp

from src import get
from src.defaults import defaults
from src.load import frompath as load


def copy(
    data: Path,
    source: Path,
    destination: Path,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> None:
    """
    Recursively copy directories listed in a JSON file from one directory to
    another.

    The primary use case is to copy selected albums (from the `wanted` list)
    from a large music library to a more curated or selective library.

    Parameters
    ----------
    data:
        Path to the JSON file, which contains a dictionary of album
        objects, each with at least the fields: artist, title, and year.
    source:
        Path to the source directory containing the albums.
    destination:
        Path to the target directory where albums will be copied.
    verbose:
        Show detailed information about the copy process, such as the
        directories being copied.
    debug:
        Enable debug-level logging for troubleshooting, showing additional
        information for debugging purposes.
    """
    if not quiet:
        print(f"""
              Moving directories registered in {data.name}
              Origin: {source}
              Destination: {destination}
              """)
    for d in load(data):
        path = get.path(d)  # Formatting `d` to its string path equivalent.
        if not quiet:
            print(f"Moving {path}.")
        fromPath = Path(source / path)
        toPath = Path(destination / path)
        cp(fromPath, toPath)
    if not quiet:
        print("Process completed.")
