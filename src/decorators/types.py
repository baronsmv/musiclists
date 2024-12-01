#!/usr/bin/env python3

import click

import src.defaults.download


def HELP(name: str, maximum: bool = False):
    return f"Types of {name} albums to download."


def TYPES(
    name: str,
    choices: tuple,
    default: tuple = ("all",),
    letter: str | None = None,
    option: str | None = None,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    if no_name_option:
        option = str()
    else:
        option = (option if option else name[:4]).lower() + "-"
    option = "--" + option + "types"
    help_message = help_message if help_message else HELP(name)
    if letter:
        return click.option(
            "-" + letter,
            option,
            type=click.Choice(("all",) + choices, case_sensitive=False),
            multiple=True,
            show_choices=True,
            default=default,
            show_default=True,
            help=help_message,
        )
    else:
        return click.option(
            option,
            type=click.Choice(("all",) + choices, case_sensitive=False),
            multiple=True,
            show_choices=True,
            default=default,
            show_default=True,
            help=help_message,
        )


def aoty(
    name: str = "AOTY",
    choices: tuple = src.defaults.download.AOTY_TYPES,
    default: tuple = ("all",),
    letter: str | None = None,
    option: str | None = None,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    return TYPES(
        name=name,
        choices=choices,
        default=default,
        letter=letter,
        option=option,
        help_message=help_message,
        no_name_option=no_name_option,
    )


def prog(
    name: str = "Progarchives",
    choices: tuple = src.defaults.download.PROG_TYPES,
    default: tuple = ("all",),
    letter: str | None = None,
    option: str | None = None,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    return TYPES(
        name=name,
        choices=choices,
        default=default,
        letter=letter,
        option=option,
        help_message=help_message,
        no_name_option=no_name_option,
    )
