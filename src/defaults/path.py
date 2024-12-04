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
DIRS = {
    "download": DATA_DIR,
    "output": OUTPUT_DIR,
    "dedup": DEDUP_DIR,
    "merge": MERGE_DIR,
}  # type: dict[str: Path]

PATH_TYPE = Literal["download", "output", "dedup", "merge"]
VALID_PATH_TYPE: Tuple[PATH_TYPE, ...] = get_args(PATH_TYPE)

for d in DIRS.values():
    d.mkdir(exist_ok=True)

LOG_PATH = Path(DATA_DIR / "musiclists.log")
