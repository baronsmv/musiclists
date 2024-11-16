#!/usr/bin/env python3

import json
from pathlib import Path

from src.defaults import defaults


def frompath(path: Path, verbose: bool = defaults.VERBOSE) -> dict:
    if verbose:
        print(f"Loading list from {path}...")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
