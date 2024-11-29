#!/usr/bin/env python3

from collections.abc import Iterator
from pathlib import Path
import re

from src.defaults import defaults
from src.load import from_path as load


def lines(
    pattern: str,
    content: str,
    end: str | None = None,
    before: int = 0,
    after: int = 0,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator:
    return re.finditer(
        (r"(.*\n){" + str(before) + "}" if before > 0 else "")
        + r".*"
        + pattern
        + r".*"
        + (r"(\n.*?){0,}" + end + r".*" if end else "")
        + (r"(\n.*){" + str(after) + "}" if after > 0 else ""),
        content,
        re.MULTILINE,
    )


def dedup(
    data1: Path,
    data2: Path,
    dedup_path: Path,
    field: str = defaults.AUTO_FIELD,
    key_sep: str = defaults.KEY_SEP,
    key_suf: str = defaults.DATA_SUFFIX,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> tuple[Path, dict[str, dict[str, str | list]], bool]:
    key = Path(dedup_path / f"{data1.stem}{key_sep}{data2.stem}.{key_suf}")
    invKey = Path(dedup_path / f"{data2.stem}{key_sep}{data1.stem}.{key_suf}")
    inv = False
    if key.exists():
        filePath = key
        data = load(filePath)  # type:dict[str, dict[str, str | list]]
    elif invKey.exists():
        filePath = invKey
        data = load(filePath)
        inv = True
    else:
        filePath = key
        data = dict()
    return filePath, data, inv
