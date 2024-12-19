#!/usr/bin/env python3

from pathlib import Path

from src.defaults import path
from src.defaults.defaults import DATA_SUFFIX


def __search__(
    directory: Path,
    postfix: str | None = None,
) -> dict[str, Path]:
    return {
        file.stem + (f".{postfix}" if postfix else ""): file
        for file in sorted(directory.glob(f"*.{DATA_SUFFIX}"))
    }


ALBUMS_DEDUP = __search__(path.ALBUMS_DEDUP, postfix="dedup")
TRACKS_DEDUP = __search__(path.TRACKS_DEDUP, postfix="dedup")
ALL_DEDUP = ALBUMS_DEDUP | TRACKS_DEDUP

ALBUMS = __search__(path.ALBUMS_DOWNLOAD)
ALBUMS_FILTERED = __search__(path.ALBUMS_FILTERED, postfix="filter")
ALBUMS_UNION = __search__(path.ALBUMS_UNION, postfix="union")
ALBUMS_INTERSECT = __search__(path.ALBUMS_INTERSECT, postfix="inter")
ALBUMS_DIFF = __search__(path.ALBUMS_DIFF, postfix="diff")
ALL_ALBUMS = (
    ALBUMS | ALBUMS_FILTERED | ALBUMS_UNION | ALBUMS_INTERSECT | ALBUMS_DIFF
)

TRACKS = __search__(path.TRACKS_DOWNLOAD)
TRACKS_FILTERED = __search__(path.TRACKS_FILTERED, postfix="filter")
TRACKS_UNION = __search__(path.TRACKS_UNION, postfix="union")
TRACKS_INTERSECT = __search__(path.TRACKS_INTERSECT, postfix="intersect")
TRACKS_DIFF = __search__(path.TRACKS_DIFF, postfix="diff")
ALL_TRACKS = (
    TRACKS | TRACKS_FILTERED | TRACKS_UNION | TRACKS_INTERSECT | TRACKS_DIFF
)

ALBUM_ID = (
    "id",
    "internal_id",
)
TRACK_ID = ("track_id",)

ALBUM_COLUMNS = {
    "id": "ID",
    "internal_id": "Int. ID",
    "artist": "Artist",
    "album": "Album",
    "year": "Year",
    "type": "Type",
    "position": "Pos.",
    "user_score": "SC",
    "user_ratings": "RT",
    "album_path": "Directory",
    "album_url": "Album URL",
    "cover_url": "Cover URL",
}
TRACK_COLUMNS = {
    "track_id": "Track ID",
    "track_score": "TSC",
    "track_ratings": "TRT",
    "track_number": "No.",
    "track_title": "Track Title",
    "track_length": "Track Length",
    "track_disc": "Disc",
    "track_path": "Filename",
    "featuring": "Featuring",
    "track_url": "Track URL",
} | ALBUM_COLUMNS

ALBUM_SORT_BY = {
    "id": False,
    "internal_id": False,
    "artist": False,
    "album": False,
    "year": False,
    "type": False,
    "position": False,
    "user_score": True,
    "user_ratings": False,
}  # True if order is DESC, False otherwise.
TRACK_SORT_BY = {
    "track_score": True,
    "track_ratings": True,
    "track_number": False,
    "track_title": False,
    "track_length": True,
    "track_disc": False,
    "featuring": False,
} | ALBUM_SORT_BY  # True if order is DESC, False otherwise.
