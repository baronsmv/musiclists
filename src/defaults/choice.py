#!/usr/bin/env python3

from pathlib import Path

from src.defaults import path
from src.defaults.defaults import DATA_SUFFIX


def __search__(
    directory: Path,
    prefix: str | None = None,
) -> dict[str, Path]:
    return {
        (f"{prefix}." if prefix else "") + file.stem: file
        for file in sorted(directory.glob(f"*.{DATA_SUFFIX}"))
    }


DL_CHOICE = __search__(path.DATA_DIR)
if "dirs" in DL_CHOICE:
    DL_CHOICE["dirs"] = DL_CHOICE.pop("dirs")
UNION_CHOICE = __search__(path.UNION_DIR, prefix="merge")
INTERSECT_CHOICE = __search__(path.INTERSECT_DIR, prefix="intersect")
DIFF_CHOICE = __search__(path.DIFF_DIR, prefix="diff")
DEDUP_CHOICE = __search__(path.DEDUP_DIR, prefix="dedup")

DATA_CHOICE = DL_CHOICE | UNION_CHOICE | INTERSECT_CHOICE | DIFF_CHOICE
ALL_CHOICE = DATA_CHOICE | DEDUP_CHOICE

ID_CHOICES = (
    "id",
    "internal_id",
)

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
