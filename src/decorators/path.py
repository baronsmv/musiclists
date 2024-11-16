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
    default_text_path: Path,
    letter: str | None = None,
    flag: str | None = None,
    text: bool = False,
    read: bool = False,
):
    if not flag:
        flag = name.lower()[:4]
    flag = f"--{flag}" + ("-text" if text else "") + "-path"
    file_type = FILE_FROM if read else FILE_TO
    default_path = default_text_path if text else default_path
    direction = "from" if read else "to"
    help_message = SAVE(
        name, default.TEXT_SUFFIX if text else default.SUFFIX, direction
    )
    if letter:
        return click.option(
            "-" + letter,
            flag,
            type=file_type,
            default=default_path,
            show_default=True,
            help=help_message,
        )
    else:
        return click.option(
            flag,
            type=file_type,
            default=default_path,
            show_default=True,
            help=help_message,
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


def aoty(letter: str | None = None, text: bool = False, read: bool = False):
    return PATH(
        name="AOTY",
        default_path=default.AOTY_PATH,
        default_text_path=default.AOTY_TEXT_PATH,
        letter=letter,
        text=text,
        read=read,
    )


def prog(letter: str | None = None, text: bool = False, read: bool = False):
    return PATH(
        name="Progarchives",
        default_path=default.PROG_PATH,
        default_text_path=default.PROG_TEXT_PATH,
        letter=letter,
        text=text,
        read=read,
    )


def merge(letter: str | None = None, text: bool = False, read: bool = False):
    return PATH(
        name="merge",
        default_path=default.MERGE_PATH,
        default_text_path=default.MERGE_TEXT_PATH,
        flag="merge",
        letter=letter,
        text=text,
        read=read,
    )


def dirs(letter: str | None = None, text: bool = False, read: bool = False):
    return PATH(
        name="directories",
        default_path=default.DIRS_PATH,
        default_text_path=default.DIRS_TEXT_PATH,
        flag="dirs",
        letter=letter,
        text=text, read=read,
    )


def wanted(letter: str | None = None, text: bool = False, read: bool = False):
    return PATH(
        name="wanted",
        default_path=default.WANTED_PATH,
        default_text_path=default.WANTED_TEXT_PATH,
        flag="wanted",
        letter=letter,
        text=text,
        read=read,
    )


def leftover(
    letter: str | None = None, text: bool = False, read: bool = False
):
    return PATH(
        name="left over",
        default_path=default.LEFTOVER_PATH,
        default_text_path=default.LEFTOVER_TEXT_PATH,
        flag="leftover",
        letter=letter,
        text=text,
        read=read,
    )
