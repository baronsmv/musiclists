#!/usr/bin/env python3

APP_NAME = "MusicLists"
VERSION = "0.2.1"

QUIET = False
VERBOSE = False
DEBUG = False

INCLUDE_NONE = False
CEIL = True
DEDUP = True
ONLY_HIGHEST_MATCH = True

ALBUM_MAX_SCORE = None
ALBUM_MIN_SCORE = None
TRACK_MAX_SCORE = None
TRACK_MIN_SCORE = None
ALBUM_MAX_RATINGS = None
ALBUM_MIN_RATINGS = None
TRACK_MAX_RATINGS = None
TRACK_MIN_RATINGS = None

ID_LENGTH = 22
ID_SEP = ""
ALBUM_REPR_SEP = " - "

AUTO_FIELD = "possible"
VERIFIED_FIELD = "verified"
DATA_SUFFIX = "polars"
TEXT_SUFFIX = "txt"

MIN_LEVEL = 0
MAX_LEVEL = 5

ALBUM_NUM_FILTER = {
    "user_score": (95, 100),
}
TRACKS_NUM_FILTER = {
    "track_score": (90, None),
    "track_ratings": (10, None),
    "user_score": (None, None),
}
