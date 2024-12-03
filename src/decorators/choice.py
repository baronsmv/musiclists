#!/usr/bin/env python3

import click

from src.defaults import choice, download


def __choice__(
    option: str,
    choices: tuple,
    help_message: str,
    all_option: bool = True,
    default: tuple = (0,),
    letter: str | None = None,
):
    if all_option:
        choices = ("all",) + choices
    if letter:
        return click.option(
            "-" + letter,
            f"--{option}",
            type=click.Choice(choices, case_sensitive=False),
            multiple=True,
            show_choices=True,
            default=tuple(choices[d] for d in default),
            show_default=True,
            help=help_message,
        )
    else:
        return click.option(
            f"--{option}",
            type=click.Choice(choices, case_sensitive=False),
            multiple=True,
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
    default: tuple = (0,),
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
    default: tuple = (0,),
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
    letter: str | None = "c",
    choices: tuple = choice.COLUMN_CHOICES,
    help_message: str = "Columns to consider for the search process.",
    all_option: bool = False,
    default: tuple = (0, 1, 2),
):
    return __choice__(
        option=option,
        choices=choices,
        help_message=help_message,
        all_option=all_option,
        default=default,
        letter=letter,
    )
