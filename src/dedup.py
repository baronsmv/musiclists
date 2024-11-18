#!/usr/bin/env python3

from collections.abc import Iterator
from difflib import SequenceMatcher

from src.defaults import defaults
from src import get


def dedup(
    data1: dict,
    data2: dict,
    lowerlimit: int | float = 0.6,
    upperlimit: int | float = 1,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.VERBOSE,
) -> Iterator[dict[str, str]]:
    """
    Compare each of the objects
    """
    for d1 in data1.values():
        for d2 in data2.values():
            a1 = get.path(d1)
            a2 = get.path(d2)
            sim = SequenceMatcher(None, a1, a2).ratio()
            if lowerlimit <= sim < upperlimit:
                yield {a1: a2}
