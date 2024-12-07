#!/usr/bin/env python3

APP_NAME = "MusicLists"
VERSION = "0.1"

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
MAX_RATINGS = None
MIN_RATINGS = None

KEY_LENGTH = 22
KEY_SEP = "-"

AUTO_FIELD = "possible"
VERIFIED_FIELD = "verified"
DATA_SUFFIX = "polars"
TEXT_SUFFIX = "txt"

MIN_LEVEL = 0
MAX_LEVEL = 5

ALBUM_NUM_FILTER = {
    "user_score": (95, 100),
}
ALBUM_SORT_BY = {
    "artist": False,
    "album": False,
    "user_score": True,
}
ALBUM_SELECT = {
    "user_score": "SC",
    "artist": "Artist",
    "album": "Album",
    "year": "Year",
}

TRACKS_NUM_FILTER = {
    "track_score": (90, None),
    "track_ratings": (10, None),
    "user_score": (None, None),
}
TRACKS_SORT_BY = {
    "artist": False,
    "title": False,
    "track_number": False,
}
TRACKS_SELECT = {
    "track_score": "SC",
    "track_number": "No.",
    "track_title": "Track Title",
    "artist": "Artist",
    "title": "Album",
    "year": "Year",
}
