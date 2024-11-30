#!/usr/bin/env python3

from pathlib import Path

import click

from src.defaults import defaults
from src.get import file

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


def __help__(
    name: str, suffix: str, direction: str, extra: str | None = None
) -> str:
    return f"""
    Path where the data of {name} albums will be {direction}, in `{suffix}`
    format""" + (
        f" ({extra})." if extra else "."
    )


def __path__(
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
    help_message = (
        help_message
        if help_message
        else __help__(
            name=name,
            suffix=defaults.DATA_SUFFIX,
            direction=direction,
            extra=None,
        )
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
    default_path: Path = file.path("aoty"),
    option: str | None = None,
    letter: str | None = None,
    read: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    return __path__(
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
    default_path: Path = file.path("prog"),
    option: str | None = None,
    letter: str | None = None,
    read: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    return __path__(
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
    default_path: Path = file.path("merge"),
    option: str | None = "merge",
    letter: str | None = None,
    read: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    return __path__(
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
    default_path: Path = file.path("dirs"),
    option: str | None = "dirs",
    letter: str | None = None,
    read: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    return __path__(
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
    default_path: Path = file.path("wanted"),
    option: str | None = "wanted",
    letter: str | None = None,
    read: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    return __path__(
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
    default_path: Path = file.path("leftover"),
    option: str | None = "leftover",
    letter: str | None = None,
    read: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    return __path__(
        name=name,
        default_path=default_path,
        option=option,
        letter=letter,
        read=read,
        help_message=help_message,
        no_name_option=no_name_option,
    )
