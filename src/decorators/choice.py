#!/usr/bin/env python3

import click

from src.defaults import choice, download


def __choice__(
    option: str,
    choices: tuple,
    help_message: str,
    all_option: bool,
    default: int | tuple,
    letter: str | None,
):
    if all_option:
        choices = ("all",) + choices
    multiple = True if isinstance(default, tuple) or all_option else False
    default = (
        tuple(choices[d] for d in default) if multiple else choices[default]
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
    choices: tuple = download.AOTY_TYPES,
    help_message: str = "Types of AOTY albums to download.",
    all_option: bool = True,
    default: int | tuple = (0,),
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
    choices: tuple = download.PROG_TYPES,
    help_message: str = "Types of ProgArchives albums to download.",
    all_option: bool = True,
    default: int | tuple = (0,),
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
    choices: tuple = tuple(choice.COLUMN_CHOICES.keys()),
    help_message: str = "Columns to consider for the search process.",
    all_option: bool = True,
    default: int | tuple = (3, 4, 5),
):
    return __choice__(
        option=option,
        choices=choices,
        help_message=help_message,
        all_option=all_option,
        default=default,
        letter=letter,
    )


def key(
    option: str = "key",
    letter: str | None = None,
    choices: tuple = choice.ID_CHOICES,
    help_message: str = "Key for the process.",
    all_option: bool = False,
    default: int | tuple = 0,
):
    return __choice__(
        option=option,
        choices=choices,
        help_message=help_message,
        all_option=all_option,
        default=default,
        letter=letter,
    )
