#!/usr/bin/env python3

from pathlib import Path

from src.defaults import path
from src.defaults.defaults import DATA_SUFFIX


def __search__(
    directory: Path,
    prefix: str | None = None,
) -> dict[str, dict[str, str | Path]]:
    return {
        (prefix + "-" if prefix else "") + file.stem: file
        for file in sorted(directory.glob(f"*.{DATA_SUFFIX}"))
    }


DL_CHOICE = __search__(path.DATA_DIR)
DIFF_CHOICE = __search__(path.DIFF_DIR, prefix="diff")
MERGE_CHOICE = __search__(path.MERGE_DIR, prefix="merge")
DEDUP_CHOICE = __search__(path.DEDUP_DIR, prefix="dedup")

DATA_CHOICE = DL_CHOICE | MERGE_CHOICE | DIFF_CHOICE
ALL_CHOICE = DATA_CHOICE | DEDUP_CHOICE

ID_CHOICES = (
    "id",
    "internal_id",
)

COLUMN_CHOICES = {
    "id": "ID",
    "internal_id": "Int. ID",
    "artist": "Artist",
    "title": "Album",
    "year": "Year",
    "type": "Type",
    "genre": "Genre",
    "position": "Pos.",
    "user_score": "Score",
    "user_ratings": "Ratings",
    "album_url": "Album URL",
    "cover_url": "Cover URL",
}
