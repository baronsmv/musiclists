#!/usr/bin/env python3

from src.decorators import choice, number, groups, data
from src.decorators.decorators import (
    command,
    no_tracklist,
    search,
    highest_match,
    dedup,
    markdown,
)


def aoty(func):
    return command(
        func,
        (
            choice.aoty(),
            number.aoty_score(letter="s"),
            number.aoty_score(letter="S", maximum=True),
            no_tracklist,
        ),
        groups.download,
    )


def prog(func):
    return command(
        func,
        (
            choice.prog(),
            number.prog_score(letter="s"),
            number.prog_score(letter="S", maximum=True),
            no_tracklist,
        ),
        groups.download,
    )


def duplicates(func):
    return command(
        func,
        (
            search,
            choice.columns(letter="c"),
            data.source(letter="d", suffix="1", default=0),
            data.source(letter="D", suffix="2", default=1),
            highest_match,
            number.similarity(),
            number.num_results(),
        ),
        groups.duplicates,
    )


def merge(func):
    return command(
        func,
        (
            data.source(letter="d", suffix="1", default=0),
            data.source(letter="D", suffix="2", default=1),
            choice.columns(
                letter="c",
            ),
            choice.key(
                letter="k",
                help_message="Key for the merge process.",
            ),
            dedup,
            choice.key(
                letter="K",
                option="dedup-key",
                help_message="Key for the dedup process.",
                default=1,
            ),
        ),
        groups.transform,
    )


def albums(func):
    return command(
        func,
        (
            data.source(letter="d"),
            markdown,
            number.albums(letter="s"),
            number.albums(letter="S", maximum=True),
            number.ratings(letter="r"),
            number.ratings(letter="R", maximum=True),
            choice.columns(
                letter="c",
                default=(9, 3, 4, 5),
                help_message="Columns to include.",
            ),
        ),
        groups.export,
    )


def tracks(func):
    return command(
        func,
        (
            markdown,
            number.tracks(letter="s"),
            number.tracks(letter="S", maximum=True),
            number.albums(letter="a", show_name=True),
            number.albums(letter="A", show_name=True, maximum=True),
            number.ratings(letter="r"),
            number.ratings(letter="R", maximum=True),
        ),
        groups.export,
    )
