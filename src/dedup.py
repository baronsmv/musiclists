#!/usr/bin/env python3

from collections.abc import Iterator
from difflib import SequenceMatcher

from src.defaults import defaults
from src import get


def dedup(
    data1: dict,
    data2: dict,
    minimum: int | float = 0.6,
    maximum: int | float = 1,
    only_highest_match: bool = defaults.ONLY_HIGHEST_MATCH,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.VERBOSE,
) -> Iterator[dict[str, str]]:
    """
    Compare each object (album) in two dictionaries containing music album
    data from two JSON files.

    Parameters
    ----------
    data1:
        A dictionary of music album objects from the first JSON file.
    data2:
        A dictionary of music album objects from the second JSON file.
    minimum:
        The minimum similarity score (inclusive).
    maximum:
        The maximum similarity score (exclusive).
    only_highest_match:
        If True, only the highest similarity match for each album in `data1`
        will be yielded. If False, all matching albums within the similarity
        range will be returned.
    verbose:
        If True, prints additional information during execution.
    debug:
        If True, prints debug-level information.

    Returns
    -------
    A generator yielding dictionaries of matching album entries where the
    similarity score between the objects falls within the specified range.

    Notes
    -----
    - The function uses difflib.SequenceMatcher to calculate the similarity
      between the album entries. The string used for the match is:
      `artist - Title (year)`. The similarity ratio ranges from 0 to 1, with
      1 indicating identical objects.
    - To fine-tune the matching process, adjust the `minimum` and
      `maximum` values. For instance, a minimum value of 0.7 and an maximum
      value of 0.9 will only match albums with a similarity score between 0.7
      (inclusive) and 0.9 (exclusive).
    - When `only_highest_match` is set to `True`, for each album in `data1`,
      only the match from `data2` with the highest similarity score will be
      returned. This can be useful when you want to minimize the number of
      matches and focus on the best possible pairings. Though, there are cases
      where each album could have more than one correct pairing.
    """
    for d1 in data1.values():
        a1 = get.path(d1)
        if only_highest_match:
            highest_ratio = 0.0
        for d2 in data2.values():
            a2 = get.path(d2)
            sim = SequenceMatcher(None, a1, a2).ratio()
            if minimum <= sim < maximum:
                if only_highest_match and sim > highest_ratio:
                    highest_match = {a1: a2}
                elif not only_highest_match:
                    yield {a1: a2}
        if highest_match:
            yield highest_match
