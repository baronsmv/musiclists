#!/usr/bin/env python3

from pathlib import Path

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

VALID_LOCATION = {"download", "output", "dedup", "merge", "diff"}

for d in DIRS.values():
    d.mkdir(exist_ok=True)

LOG_PATH = Path(DATA_DIR / "musiclists.log")
