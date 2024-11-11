#!/usr/bin/env python3

from dateutil.parser import parse
from pathlib import Path


def verify(path: Path, dir: bool = False):
    if not path.exists():
        print(f"'{path}' no existe.")
        exit(1)
    if dir and not path.is_dir():
        print(f"'{path}' no es un directorio.")
        exit(1)


def isdate(string: str, fuzzy: bool = False) -> bool:
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try:
        parse(string, fuzzy=fuzzy)
        return True
    except ValueError:
        return False


def containsdirs(path: Path):
    for c in path.iterdir():
        if c.is_dir():
            return True
    return False
