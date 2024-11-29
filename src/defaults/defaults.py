#!/usr/bin/env python3

from pathlib import Path

PROG_NAME = "MusicLists"
VERSION = "0.1"

HEADERS_COLOR = "yellow"
OPTIONS_COLOR = "green"

AOTY_TYPES = ("LP", "EP", "Mixtape", "Compilation", "Live", "Soundtrack")
PROG_TYPES = (
    "Studio", "DVD", "Boxset,Compilation", "Live", "Singles,EPs,FanClub,Promo"
)

QUIET = False
VERBOSE = False
DEBUG = False

INCLUDE_NONE = False
NO_TRACKLIST = False
DEDUP = True
ONLY_HIGHEST_MATCH = True

AOTY_MAX_SCORE = 100
AOTY_MIN_SCORE = 83
PROG_MAX_SCORE = 5.0
PROG_MIN_SCORE = 3.95

KEY_LENGTH = 14
KEY_SEP = "-"

AUTO_FIELD = "possible"
VERIFIED_FIELD = "verified"
DATA_SUFFIX = "polars"
TEXT_SUFFIX = "txt"

MIN_LEVEL = 1
MAX_LEVEL = 4

CURRENT_DIR = Path(__file__).parent
SRC_DIR = CURRENT_DIR.parent
ROOT_DIR = SRC_DIR.parent
DATA_DIR = Path(ROOT_DIR / "data")
EXPORT_DIR = Path(ROOT_DIR / "export")
DEDUP_DIR = Path(ROOT_DIR / "dedup")
DIRS = (
    DATA_DIR,
    DEDUP_DIR,
    EXPORT_DIR,
)  # type: tuple[Path, ...]
for d in DIRS:
    d.mkdir(exist_ok=True)


def PATH(
    name: str,
    suffix: str | None = DATA_SUFFIX,
    export: bool = False,
) -> Path:
    return Path(
        (
            EXPORT_DIR if export else DATA_DIR
        ) / (name + ("." + suffix if suffix else ""))
    )


AOTY_PATH = PATH("aoty")
PROG_PATH = PATH("prog")
MERGE_PATH = PATH("merge")
DIRS_PATH = PATH("dirs")
WANTED_PATH = PATH("wanted")
LEFTOVER_PATH = PATH("leftover")


DL_CHOICES = {
    "aoty": AOTY_PATH,
    "prog": PROG_PATH,
}  # type: dict[str, Path]

MERGE_CHOICE = {"all": MERGE_PATH}

DATA_CHOICES = {
    k: v
    for k, v
    in (MERGE_CHOICE | DL_CHOICES).items()
    if v.exists()
}  # type: dict[str, Path]
