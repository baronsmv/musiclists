#!/usr/bin/env python3

from pathlib import Path

import click

from src.defaults.choice import DATA_CHOICE


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
                tuple(DATA_CHOICE.keys()),
                case_sensitive=False,
            ),
            show_choices=True,
            default=tuple(DATA_CHOICE.keys())[default],
            show_default=True,
            help=help_message,
        )
    else:
        return click.option(
            f"--{parameter}",
            type=click.Choice(
                tuple(DATA_CHOICE.keys()),
                case_sensitive=False,
            ),
            show_choices=True,
            default=tuple(DATA_CHOICE.keys())[default],
            show_default=True,
            help=help_message,
        )


def path(
    name: str = "path",
    exists: bool = True,
    is_file: bool = False,
):
    return click.argument(
        name,
        type=click.Path(
            exists=exists,
            file_okay=is_file,
            dir_okay=not is_file,
            path_type=Path,
        ),
    )
