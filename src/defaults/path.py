#!/usr/bin/env python3

from pathlib import Path
from typing import Literal, Tuple, get_args

CURRENT_DIR = Path(__file__).parent
SRC_DIR = CURRENT_DIR.parent
ROOT_DIR = SRC_DIR.parent

DATA_DIR = Path(ROOT_DIR / "data")
OUTPUT_DIR = Path(ROOT_DIR / "output")
DEDUP_DIR = Path(DATA_DIR / "dedup")
MERGE_DIR = Path(DATA_DIR / "merge")
DIFF_DIR = Path(DATA_DIR / "diff")

DIRS = {
    "download": DATA_DIR,
    "output": OUTPUT_DIR,
    "dedup": DEDUP_DIR,
    "merge": MERGE_DIR,
    "diff": DIFF_DIR,
}  # type: dict[str: Path]

LOCATION = Literal["download", "output", "dedup", "merge", "diff"]
VALID_LOCATION: Tuple[LOCATION, ...] = get_args(LOCATION)

for d in DIRS.values():
    d.mkdir(exist_ok=True)

LOG_PATH = Path(DATA_DIR / "musiclists.log")
