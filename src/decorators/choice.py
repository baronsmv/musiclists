#!/usr/bin/env python3

import click

from src.defaults.choice import (
    TRACK_SORT_BY,
    TRACK_COLUMNS,
    ALBUM_SORT_BY,
    ALBUM_COLUMNS,
    ID_CHOICES,
)
from src.defaults.download import AOTY_TYPES, PROG_TYPES


def __choice__(
    option: str,
    choices: tuple | dict,
    help_message: str,
    all_option: bool,
    default: str | int | tuple,
    letter: str | None,
):
    if isinstance(choices, dict):
        choices = tuple(choices.keys())
    if all_option:
        choices = ("all",) + choices
    multiple = True if isinstance(default, tuple) or all_option else False
    if isinstance(default, int) or isinstance(default[0], int):
        default = (
            tuple(choices[d] for d in default)
            if isinstance(default, tuple)
            else choices[default]
        )
    if letter:
        return click.option(
            "-" + letter,
            f"--{option}",
            type=click.Choice(choices, case_sensitive=False),
            multiple=multiple,
            show_choices=True,
            default=default,
            show_default=True,
            help=help_message,
        )
    else:
        return click.option(
            f"--{option}",
            type=click.Choice(choices, case_sensitive=False),
            multiple=multiple,
            show_choices=True,
            default=default,
            show_default=True,
            help=help_message,
        )


def aoty(
    option: str = "types",
    letter: str | None = "t",
    choices: tuple = AOTY_TYPES,
    help_message: str = "Types of AOTY albums to download.",
    all_option: bool = True,
    default: str | int | tuple = (0,),
):
    return __choice__(
        option=option,
        choices=choices,
        help_message=help_message,
        all_option=all_option,
        default=default,
        letter=letter,
    )


def prog(
    option: str = "types",
    letter: str | None = "t",
    choices: tuple = PROG_TYPES,
    help_message: str = "Types of ProgArchives albums to download.",
    all_option: bool = True,
    default: str | int | tuple = (0,),
):
    return __choice__(
        option=option,
        choices=choices,
        help_message=help_message,
        all_option=all_option,
        default=default,
        letter=letter,
    )


def columns(
    option: str = "columns",
    letter: str | None = None,
    help_msg: str = "Columns to consider for the process.",
    all_option: bool = True,
    tracks: bool = False,
    sorting: bool = False,
    default: str | int | tuple = (3, 4, 5),
):
    if tracks:
        choices = TRACK_SORT_BY if sorting else TRACK_COLUMNS
    else:
        choices = ALBUM_SORT_BY if sorting else ALBUM_COLUMNS
    return __choice__(
        option=option,
        choices=choices,
        help_message=help_msg,
        all_option=all_option,
        default=default,
        letter=letter,
    )


def key(
    option: str = "key",
    letter: str | None = None,
    choices: tuple = ID_CHOICES,
    help_message: str = "Key for the process.",
    all_option: bool = False,
    default: str | int | tuple = 0,
):
    return __choice__(
        option=option,
        choices=choices,
        help_message=help_message,
        all_option=all_option,
        default=default,
        letter=letter,
    )
