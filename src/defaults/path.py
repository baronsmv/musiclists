#!/usr/bin/env python3

from pathlib import Path
from typing import Literal

DEFAULTS = Path(__file__).parent
SRC = DEFAULTS.parent
ROOT = SRC.parent
DATA = ROOT / "data"
OUTPUT = ROOT / "output"

DEDUP = DATA / "dedup"
ALBUMS = DATA / "albums"
TRACKS = DATA / "tracks"

ALBUMS_DEDUP = DEDUP / "albums"
TRACKS_DEDUP = DEDUP / "tracks"

ALBUMS_DOWNLOAD = ALBUMS / "download"
ALBUMS_FILTERED = ALBUMS / "filtered"
ALBUMS_UNION = ALBUMS / "union"
ALBUMS_INTERSECT = ALBUMS / "intersect"
ALBUMS_DIFF = ALBUMS / "diff"
ALBUMS_OUTPUT = OUTPUT / "albums"

TRACKS_DOWNLOAD = TRACKS / "download"
TRACKS_FILTERED = TRACKS / "filtered"
TRACKS_UNION = TRACKS / "union"
TRACKS_INTERSECT = TRACKS / "intersect"
TRACKS_DIFF = TRACKS / "diff"
TRACKS_OUTPUT = OUTPUT / "tracks"

ALL_PARENTS = {
    "data": DATA,
    "output": OUTPUT,
    "dedup": DEDUP,
    "albums": ALBUMS,
    "tracks": TRACKS,
}
ALBUMS_LOCATIONS = {
    "albums-download": ALBUMS_DOWNLOAD,
    "albums-dedup": ALBUMS_DEDUP,
    "albums-filtered": ALBUMS_FILTERED,
    "albums-union": ALBUMS_UNION,
    "albums-intersect": ALBUMS_INTERSECT,
    "albums-diff": ALBUMS_DIFF,
    "albums-output": ALBUMS_OUTPUT,
}
TRACKS_LOCATIONS = {
    "tracks-download": TRACKS_DOWNLOAD,
    "tracks-dedup": TRACKS_DEDUP,
    "tracks-filtered": TRACKS_FILTERED,
    "tracks-union": TRACKS_UNION,
    "tracks-intersect": TRACKS_INTERSECT,
    "tracks-diff": TRACKS_DIFF,
    "tracks-output": TRACKS_OUTPUT,
}
DATA_LOCATIONS = ALBUMS_LOCATIONS | TRACKS_LOCATIONS
ALL = ALL_PARENTS | DATA_LOCATIONS

for d in ALL.values():
    d.mkdir(exist_ok=True)

VALID_LOCATIONS = set(ALL)
VALID_TYPES = {"albums", "tracks"}

LOCATION = Literal[
    "download", "dedup", "filtered", "union", "intersect", "diff", "output"
]
TYPE = Literal["albums", "tracks"]

LOG_PATH = DATA / "musiclists.log"
