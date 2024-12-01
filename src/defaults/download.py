#!/usr/bin/env python3

from pathlib import Path

from src.defaults.defaults import DATA_DIR, DATA_SUFFIX

AOTY_TYPES = ("LP", "EP", "Mixtape", "Compilation", "Live", "Soundtrack")
PROG_TYPES = (
    "Studio",
    "DVD",
    "Boxset,Compilation",
    "Live",
    "Singles,EPs,FanClub,Promo",
)

AOTY_MAX_SCORE = 100
AOTY_MIN_SCORE = 83
PROG_MAX_SCORE = 5.0
PROG_MIN_SCORE = 3.95

DL_CHOICES = {
    "aoty": Path(DATA_DIR / f"aoty.{DATA_SUFFIX}"),
    "prog": Path(DATA_DIR / f"prog.{DATA_SUFFIX}"),
}  # type: dict[str, Path]
