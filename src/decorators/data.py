#!/usr/bin/env python3

import click

from src.defaults import defaults


def source(
    letter: str | None = None,
    parameter: str = "data",
    suffix: str | None = None,
    default: int = 0,
):
    help_message = (
        "Source for the data" + (" " + suffix if suffix else "") + "."
    )
    if suffix:
        parameter += f"-{suffix}"
    if letter:
        return click.option(
            f"-{letter}",
            f"--{parameter}",
            type=click.Choice(
                tuple(defaults.DATA_CHOICES.keys()), case_sensitive=False
            ),
            show_choices=True,
            default=tuple(defaults.DATA_CHOICES.keys())[default],
            show_default=True,
            help=help_message,
        )
    else:
        return click.option(
            f"--{parameter}",
            type=click.Choice(
                tuple(defaults.DATA_CHOICES.keys()), case_sensitive=False
            ),
            show_choices=True,
            default=tuple(defaults.DATA_CHOICES.keys())[default],
            show_default=True,
            help=help_message,
        )