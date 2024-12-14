#!/usr/bin/env python3

from src.decorators import choice, number, groups, data
from src.decorators.decorators import (
    command,
    ceil,
    search,
    highest_match,
    dedup,
    markdown,
)
from src.defaults.choice import (
    DATA_CHOICE,
    TRACK_COLUMNS,
    ALBUM_SORT_BY,
    TRACK_SORT_BY,
)
from src.defaults.defaults import (
    ALBUM_MIN_SCORE,
    ALBUM_MAX_SCORE,
    TRACK_MIN_SCORE,
    TRACK_MAX_SCORE,
    ALBUM_MIN_RATINGS,
    ALBUM_MAX_RATINGS,
    TRACK_MIN_RATINGS,
    TRACK_MAX_RATINGS,
)


def aoty(func):
    return command(
        func,
        (
            choice.aoty(),
            number.aoty_score(letter="s"),
            number.aoty_score(letter="S", maximum=True),
        ),
        groups.download,
    )


def prog(func):
    return command(
        func,
        (
            choice.prog(),
            ceil,
            number.prog_score(letter="s"),
            number.prog_score(letter="S", maximum=True),
        ),
        groups.download,
    )


def dirs(func):
    return command(
        func,
        (data.path(),),
        groups.download,
    )


def duplicates(func):
    if len(DATA_CHOICE) < 2:
        return func
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
    if len(DATA_CHOICE) < 2:
        return func
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


def diff(func):
    if len(DATA_CHOICE) < 2:
        return func
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
                help_message="Key for the diff process.",
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
            number.albums(letter="s", default=ALBUM_MIN_SCORE),
            number.albums(letter="S", default=ALBUM_MAX_SCORE, maximum=True),
            number.ratings(letter="r", default=ALBUM_MIN_RATINGS),
            number.ratings(
                letter="R", default=ALBUM_MAX_RATINGS, maximum=True
            ),
            choice.columns(
                letter="c",
                default=("user_score", "artist", "album", "year", "type"),
                help="Columns to include.",
            ),
            choice.columns(
                option="sort-by",
                choices=ALBUM_SORT_BY,
                default=("id",),
                all_option=False,
                help="Columns to sort by.",
            ),
        ),
        groups.export,
    )


def tracks(func):
    return command(
        func,
        (
            data.source(letter="d"),
            markdown,
            number.tracks(letter="s", default=TRACK_MIN_SCORE),
            number.tracks(letter="S", default=TRACK_MAX_SCORE, maximum=True),
            number.albums(letter="a", default=ALBUM_MIN_SCORE, show_name=True),
            number.albums(
                letter="A",
                default=ALBUM_MAX_SCORE,
                show_name=True,
                maximum=True,
            ),
            number.ratings(letter="r", default=TRACK_MIN_RATINGS),
            number.ratings(
                letter="R", default=TRACK_MAX_RATINGS, maximum=True
            ),
            choice.columns(
                letter="c",
                choices=TRACK_COLUMNS,
                default=(
                    "track_score",
                    "track_number",
                    "track_title",
                    "internal_id",
                    "artist",
                    "album",
                ),
                help="Columns to include.",
            ),
            choice.columns(
                option="sort-by",
                choices=TRACK_SORT_BY,
                default=("id", "track_score"),
                all_option=False,
                help="Columns to sort by.",
            ),
        ),
        groups.export,
    )
