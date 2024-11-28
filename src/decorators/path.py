#!/usr/bin/env python3

import click
from pathlib import Path

from src.defaults import defaults

EXISTING_DIR = click.Path(
    exists=True,
    dir_okay=True,
    path_type=Path,
)
NEW_DIR = click.Path(
    exists=False,
    dir_okay=True,
    path_type=Path,
)
FILE_TO = click.Path(
    exists=False,
    dir_okay=False,
    writable=True,
    path_type=Path,
)
FILE_FROM = click.Path(
    exists=True,
    dir_okay=False,
    readable=True,
    path_type=Path,
)


def HELP(
    name: str, suffix: str, direction: str, extra: str | None = None
) -> str:
    return f"""
    Path where the data of {name} albums will be {direction}, in `{suffix}`
    format""" + (
        f" ({extra})." if extra else "."
    )


def PATH(
    name: str,
    default_path: Path,
    letter: str | None = None,
    option: str | None = None,
    read: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    if no_name_option:
        option = str()
    else:
        option = (option if option else name[:4]).lower() + "-"
    option = "--" + option + "path"
    file_type = FILE_FROM if read else FILE_TO
    default_path = default_path
    direction = "loaded from" if read else "stored"
    help_message = help_message if help_message else HELP(
        name=name,
        suffix=defaults.SUFFIX,
        direction=direction,
        extra=None,
    )
    if letter:
        return click.option(
            "-" + letter,
            option,
            type=file_type,
            default=default_path,
            show_default=True,
            help=help_message,
        )
    else:
        return click.option(
            option,
            type=file_type,
            default=default_path,
            show_default=True,
            help=help_message,
        )


source = click.argument(
    "source_path",
    type=EXISTING_DIR,
)
destination = click.argument(
    "destination_path",
    type=NEW_DIR,
)
dedup = click.option(
    "--dedup-path",
    type=NEW_DIR,
    default=defaults.DEDUP_DIR,
    show_default=True,
    help="Directory of deduplicates files.",
)


def aoty(
    name: str = "AOTY",
    default_path: Path = defaults.AOTY_PATH,
    option: str | None = None,
    letter: str | None = None,
    read: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    return PATH(
        name=name,
        default_path=default_path,
        option=option,
        letter=letter,
        read=read,
        help_message=help_message,
        no_name_option=no_name_option,
    )


def prog(
    name: str = "Progarchives",
    default_path: Path = defaults.PROG_PATH,
    option: str | None = None,
    letter: str | None = None,
    read: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    return PATH(
        name=name,
        default_path=default_path,
        option=option,
        letter=letter,
        read=read,
        help_message=help_message,
        no_name_option=no_name_option,
    )


def merge(
    name: str = "merge",
    default_path: Path = defaults.MERGE_PATH,
    option: str | None = "merge",
    letter: str | None = None,
    read: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    return PATH(
        name=name,
        default_path=default_path,
        option=option,
        letter=letter,
        read=read,
        help_message=help_message,
        no_name_option=no_name_option,
    )


def dirs(
    name: str = "directories",
    default_path: Path = defaults.DIRS_PATH,
    option: str | None = "dirs",
    letter: str | None = None,
    read: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    return PATH(
        name=name,
        default_path=default_path,
        option=option,
        letter=letter,
        read=read,
        help_message=help_message,
        no_name_option=no_name_option,
    )


def wanted(
    name: str = "wanted",
    default_path: Path = defaults.WANTED_PATH,
    option: str | None = "wanted",
    letter: str | None = None,
    read: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    return PATH(
        name=name,
        default_path=default_path,
        option=option,
        letter=letter,
        read=read,
        help_message=help_message,
        no_name_option=no_name_option,
    )


def leftover(
    name: str = "leftover",
    default_path: Path = defaults.LEFTOVER_PATH,
    option: str | None = "leftover",
    letter: str | None = None,
    read: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    return PATH(
        name=name,
        default_path=default_path,
        option=option,
        letter=letter,
        read=read,
        help_message=help_message,
        no_name_option=no_name_option,
    )
