#!/usr/bin/env python3

from pathlib import Path

from src.defaults.defaults import DATA_SUFFIX
from src.defaults.path import DATA_DIR

DL_CHOICES = {
    name: Path(DATA_DIR / str(name + "." + DATA_SUFFIX))
    for name in ("aoty", "prog")
}
MERGE_CHOICE = {"all": Path(DATA_DIR / f"merge.{DATA_SUFFIX}")}

DATA_CHOICES = {
    k: v for k, v in (MERGE_CHOICE | DL_CHOICES).items() if v.exists()
}  # type: dict[str, Path]
