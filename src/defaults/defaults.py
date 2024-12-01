#!/usr/bin/env python3

from pathlib import Path

from src.defaults.download import DL_CHOICES

APP_NAME = "MusicLists"
VERSION = "0.1"

QUIET = False
VERBOSE = False
DEBUG = False

INCLUDE_NONE = False
NO_TRACKLIST = False
DEDUP = True
ONLY_HIGHEST_MATCH = True

ALBUM_MAX_SCORE = None
ALBUM_MIN_SCORE = None
TRACK_MAX_SCORE = None
TRACK_MIN_SCORE = None
MAX_RATINGS = None
MIN_RATINGS = None

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
OUTPUT_DIR = Path(ROOT_DIR / "output")
DEDUP_DIR = Path(DATA_DIR / "dedup")
DIRS = (
    DATA_DIR,
    DEDUP_DIR,
    OUTPUT_DIR,
)  # type: tuple[Path, ...]
for d in DIRS:
    d.mkdir(exist_ok=True)

MERGE_CHOICE = {"all": Path(DATA_DIR / f"merge.{DATA_SUFFIX}")}

DATA_CHOICES = {
    k: v for k, v in (MERGE_CHOICE | DL_CHOICES).items() if v.exists()
}  # type: dict[str, Path]
