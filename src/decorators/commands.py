#!/usr/bin/env python3

from src.decorators import choice, number, groups, data
from src.decorators.decorators import (
    command,
    ceil,
    highest_match,
    use_dedup,
    markdown,
    search,
    name,
)
from src.defaults.choice import ALL_ALBUMS, ALL_TRACKS
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

__albums_filters__ = (
    (
        data.source(letter="d"),
        name,
        number.albums_score(letter="s", default=ALBUM_MIN_SCORE),
        number.albums_score(letter="S", default=ALBUM_MAX_SCORE, maximum=True),
        number.ratings(letter="r", default=ALBUM_MIN_RATINGS),
        number.ratings(letter="R", default=ALBUM_MAX_RATINGS, maximum=True),
        choice.columns(
            letter="c",
            default=("user_score", "artist", "album", "year", "type"),
            help_msg="Columns to include.",
        ),
        choice.columns(
            letter="C",
            option="sort-by",
            sorting=True,
            default=("id",),
            all_option=False,
            help_msg="Columns to sort by.",
        ),
        number.limit_per_column(name="artist", letter="A"),
        number.limit_per_column(name="year", letter="y"),
    )
    if len(ALL_ALBUMS) >= 1
    else ()
)
__tracks_filters__ = (
    (
        data.source(letter="d", tracks=True),
        name,
        number.tracks_score(letter="s", default=TRACK_MIN_SCORE),
        number.tracks_score(letter="S", default=TRACK_MAX_SCORE, maximum=True),
        number.albums_score(default=ALBUM_MIN_SCORE, show_name=True),
        number.albums_score(
            default=ALBUM_MAX_SCORE,
            show_name=True,
            maximum=True,
        ),
        number.ratings(letter="r", default=TRACK_MIN_RATINGS),
        number.ratings(letter="R", default=TRACK_MAX_RATINGS, maximum=True),
        choice.columns(
            letter="c",
            tracks=True,
            default=(
                "track_score",
                "track_number",
                "track_title",
                "artist",
                "album",
                "year",
            ),
            help_msg="Columns to include.",
        ),
        choice.columns(
            letter="C",
            option="sort-by",
            tracks=True,
            sorting=True,
            default=("id", "track_score"),
            all_option=False,
            help_msg="Columns to sort by.",
        ),
        number.limit_per_column(name="album", letter="a", entries="albums"),
        number.limit_per_column(name="artist", letter="A", entries="tracks"),
        number.limit_per_column(name="year", letter="y", entries="tracks"),
    )
    if len(ALL_TRACKS) >= 1
    else ()
)
__albums_source__ = (
    (
        data.source(letter="d", suffix="1", default=0),
        data.source(letter="D", suffix="2", default=1),
        name,
        choice.columns(letter="c"),
    )
    if len(ALL_ALBUMS) >= 2
    else ()
)
__tracks_source__ = (
    (
        data.source(letter="d", suffix="1", default=0, tracks=True),
        data.source(letter="D", suffix="2", default=1, tracks=True),
        name,
        choice.columns(letter="c", tracks=True),
    )
    if len(ALL_TRACKS) >= 2
    else ()
)
__dedup__ = (
    use_dedup,
    choice.key(
        letter="K",
        option="dedup-key",
        help_message="Key for the dedup process.",
        default="internal_id",
    ),
)


def download_aoty(func):
    return command(
        func,
        decorators=(
            choice.aoty(),
            number.aoty_score(letter="s"),
            number.aoty_score(letter="S", maximum=True),
        ),
        group=groups.download,
        name_="aoty",
    )


def download_prog(func):
    return command(
        func,
        decorators=(
            choice.prog(),
            ceil,
            number.prog_score(letter="s"),
            number.prog_score(letter="S", maximum=True),
        ),
        group=groups.download,
        name_="prog",
    )


def get(func):
    return command(
        func,
        decorators=(data.path(),),
        group=groups.files,
    )


def dedup_find(func):
    if len(ALL_ALBUMS) < 2:
        return func
    return command(
        func,
        decorators=(
            search,
            choice.columns(letter="c"),
            data.source(letter="d", suffix="1", default=0),
            data.source(letter="D", suffix="2", default=1),
            highest_match,
            number.similarity(),
            number.num_results(),
        ),
        group=groups.duplicates,
        name_="find",
    )


def __transform__(
    func,
    name_: str,
    filters: bool = False,
    dedup: bool = True,
    tracks: bool = False,
):
    if len(ALL_TRACKS if tracks else ALL_ALBUMS) < (1 if filters else 2):
        return func
    return command(
        func,
        decorators=(__tracks_filters__ if tracks else __albums_filters__)
        if filters
        else (
            *(__tracks_source__ if tracks else __albums_source__),
            choice.key(
                letter="k",
                tracks=tracks,
                help_message=f"Key for the {name_} process.",
            ),
            *(__dedup__ if dedup and not filters else ()),
        ),
        group=groups.tracks if tracks else groups.albums,
        name_=name_,
    )


def albums_filter(func):
    return __transform__(func, name_="filter", filters=True)


def tracks_filter(func):
    return __transform__(func, name_="filter", filters=True, tracks=True)


def albums_union(func):
    return __transform__(func, name_="union")


def tracks_union(func):
    return __transform__(func, name_="union", tracks=True)


def albums_intersect(func):
    return __transform__(func, name_="intersect", dedup=False)


def tracks_intersect(func):
    return __transform__(func, name_="intersect", dedup=False, tracks=True)


def albums_diff(func):
    return __transform__(func, name_="diff")


def tracks_diff(func):
    return __transform__(func, name_="diff", tracks=True)


def __export__(func, tracks: bool = False):
    return command(
        func,
        decorators=(
            markdown,
            *(__tracks_filters__ if tracks else __albums_filters__),
        ),
        group=groups.export,
        name_="tracks" if tracks else "albums",
    )


def export_albums(func):
    return __export__(func)


def export_tracks(func):
    return __export__(func, tracks=True)


def playlist(func):
    return command(
        func,
        decorators=(
            data.source(letter="d", default=0, tracks=True),
            data.path(exists=False, is_file=True),
        ),
        group=groups.files,
    )
