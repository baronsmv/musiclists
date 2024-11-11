#!/usr/bin/env python3

from collections.abc import Iterator
from pathlib import Path
import re

from src.load import frompath as load


DEFAULT_KEY_SEP = "-"
DEFAULT_SUFFIX = "json"
DEFAULT_AUTO_FIELD = "possible"
DEFAULT_VERIFIED_FIELD = "verified"


def lines(
    pattern: str, content: str, before: int = 0, after: int = 0
) -> Iterator:
    return re.finditer(
        (r"(.*\n){" + str(before) + "}" if before > 0 else "")
        + r".*"
        + pattern
        + r".*"
        + (r"(\n.*){" + str(after) + "}" if after > 0 else ""),
        content,
        re.MULTILINE,
    )


def dedup(
    data1: Path,
    data2: Path,
    dedupdir: Path,
    field: str = DEFAULT_AUTO_FIELD,
    keysep: str = DEFAULT_KEY_SEP,
    keysuffix: str = DEFAULT_SUFFIX,
) -> tuple[Path, dict[str, dict[str, str | list]], bool]:
    key = Path(dedupdir / f"{data1.stem}{keysep}{data2.stem}.{keysuffix}")
    invKey = Path(dedupdir / f"{data2.stem}{keysep}{data1.stem}.{keysuffix}")
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
