#!/usr/bin/env python3

import click
from pathlib import Path

from src.defaults import defaults as default

EXISTING_DIR = click.Path(
    exists=True, dir_okay=True, path_type=Path,
)
NEW_DIR = click.Path(
    exists=False, dir_okay=True, path_type=Path,
)
FILE_TO = click.Path(
    exists=False, dir_okay=False, writable=True, path_type=Path,
)
FILE_FROM = click.Path(
    exists=True, dir_okay=False, readable=True, path_type=Path,
)


def SAVE(name: str, suffix: str, direction: str) -> str:
    return f"Path to save {name} {suffix} file {direction}."


def PATH(
    name: str,
    default_path: Path,
    flag: str | None = None,
    text: bool = False,
    read: bool = False,
):
    if not flag:
        flag = name.lower()[:4]
    direction = "from" if read else "to"
    return click.option(
        f"--{flag}" + "-text" if text else "" + "-path",
        type=FILE_FROM if read else FILE_TO,
        default=default_path,
        show_default=True,
        help=SAVE(
            name, default.TEXT_SUFFIX if text else default.SUFFIX, direction
        ),
    )


music = click.argument(
    "music_path",
    type=EXISTING_DIR,
)
destination = click.argument(
    "destination_path",
    type=NEW_DIR,
)
dedup = click.option(
    "--dedup-path",
    type=NEW_DIR,
    default=default.DEDUP_DIR,
    show_default=True,
    help="Directory of deduplicates files.",
)


def aoty(text: bool = False, read: bool = False):
    return PATH("AOTY", default.AOTY_PATH, text=text, read=read)


def prog(text: bool = False, read: bool = False):
    return PATH("Progarchives", default.AOTY_PATH, text=text, read=read)


def merge(text: bool = False, read: bool = False):
    return PATH(
        "merge", default.MERGE_PATH, flag="merge", text=text, read=read
    )


def dirs(text: bool = False, read: bool = False):
    return PATH(
        "directories", default.DIRS_PATH, flag="dirs", text=text, read=read
    )


def wanted(text: bool = False, read: bool = False):
    return PATH("wanted", default.WANTED_PATH, text=text, read=read)


def leftover(text: bool = False, read: bool = False):
    return PATH("left over", default.LEFTOVER_PATH, text=text, read=read)
