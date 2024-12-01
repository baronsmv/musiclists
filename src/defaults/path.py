#!/usr/bin/env python3

from pathlib import Path

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
