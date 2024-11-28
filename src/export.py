#!/usr/bin/env python3

from polars import DataFrame
from pathlib import Path

from src.load import from_path as load
from src.defaults import defaults


def export(
    path: Path,
    new_path: Path,
):
    df = load(path)
    df.
