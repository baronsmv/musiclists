#!/usr/bin/env python3

import multiprocessing.dummy as mp
from datetime import timedelta
from textwrap import dedent

from src import dump
from src.classes.MusicList import MusicList
from src.defaults import defaults
from src.defaults.download import (
    AOTY_TYPES,
    AOTY_MIN_SCORE,
    AOTY_MAX_SCORE,
    PROG_TYPES,
    PROG_MIN_SCORE,
    PROG_MAX_SCORE,
)
from src.get import data as get_data


def __download__(
    name: str,
    function,
    type_1,
    type_2,
    score_key: str,
    min_score: int | float,
    max_score: int | float,
    website_name: str | None = None,
    ceil: bool = defaults.CEIL,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    if verbose:
        print(
            dedent(
                f"""
            Download process started:
            - Types: {(
                    type_1 if isinstance(type_1, int) else
                    tuple(t[0] for t in type_1)
                    if isinstance(type_1[0], tuple)
                    else type_1
                )}
            - Types: {(
                    type_2 if isinstance(type_2, int) else
                    tuple(t[0] for t in type_2)
                    if isinstance(type_2[0], tuple)
                    else type_2
                )}
            - Minimum score: {min_score}
            - Maximum score: {max_score}
            """
            )
        )
    if not quiet:
        if website_name:
            print(f"Downloading lists from {website_name}:")
        else:
            print("Downloading lists:")
    data = (
        list()
    )  # type: list[dict[str, str | int | float | list | dict | timedelta]]
    until = dump.until(
        function=function,
        type1=type_1,
        type2=type_2,
        score_key=score_key,
        min_score=min_score,
        max_score=max_score,
        ceil=ceil,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )
    multithread = False
    if multithread:
        with mp.Pool(4) as executor:
            executor.map(data.append, until)
    else:
        for album in until:
            data.append(album)
    ml = MusicList(data)
    ml.save(name)
    ml.tracks().save()


def aoty(
    field: str = "aoty",
    types: tuple = AOTY_TYPES,
    start_page: int = 1,
    min_score: int = AOTY_MIN_SCORE,
    max_score: int = AOTY_MAX_SCORE,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    __download__(
        name=field,
        function=dump.aoty,
        type_1=types,
        type_2=start_page,
        score_key="user_score",
        min_score=min_score,
        max_score=max_score,
        website_name="AOTY",
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )


def prog(
    field: str = "prog",
    types: tuple = tuple(PROG_TYPES.keys()),
    min_score: float = PROG_MIN_SCORE,
    max_score: float = PROG_MAX_SCORE,
    ceil: bool = defaults.CEIL,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    if not quiet:
        print("Generating list of genres...")
    __download__(
        name=field,
        function=dump.prog,
        type_1=tuple(get_data.prog_genres().items()),
        type_2=tuple((t, PROG_TYPES[t]) for t in types),
        score_key="user_score",
        min_score=min_score,
        max_score=max_score,
        website_name="Progarchives",
        ceil=ceil,
        quiet=quiet,
        verbose=verbose,
        debug=debug,
    )
