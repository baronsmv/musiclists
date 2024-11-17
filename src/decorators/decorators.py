#!/usr/bin/env python3

import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand, version_option
from functools import wraps
from time import time

from src.decorators import path
from src.defaults import defaults


@click.group(
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green",
)
def cli() -> None:
    pass


def count_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        print(f"Program concluded in {round(time() - start, 2)} seconds.")
        return result
    return wrapper


def LOWER_LIMIT(name: str):
    return f"Lower limit for {name} score."


comm = cli.command(
    cls=HelpColorsCommand,
)
version = version_option(
    version=defaults.VERSION,
    prog_name=defaults.PROG_NAME,
    message_color="green"
)
verbose = click.option(
    "-v",
    "--verbose",
    is_flag=True,
    type=click.BOOL,
    default=defaults.VERBOSE,
    show_default=True,
    help="Show detailed information about the process.",
)
debug = click.option(
    "--debug",
    is_flag=True,
    type=click.BOOL,
    default=defaults.DEBUG,
    show_default=True,
    help="Enable debug-level logging for troubleshooting.",
)
text = click.option(
    "-t",
    "--text",
    is_flag=True,
    type=click.BOOL,
    default=defaults.TEXT,
    show_default=True,
    help="Output the list as a text file as well.",
)
deduplic = click.option(
    "-d",
    "--dedup/--no-dedup",
    is_flag=True,
    type=click.BOOL,
    default=True,
    show_default=True,
    help="Deduplicate the output based on its deduplicates file.",
)
aoty_lower = click.option(
    "--aoty-lower",
    type=click.INT,
    default=defaults.AOTY_SCORE,
    show_default=True,
    help=LOWER_LIMIT("AOTY"),
)
prog_lower = click.option(
    "--prog-lower",
    type=click.FLOAT,
    default=defaults.PROG_SCORE,
    show_default=True,
    help=LOWER_LIMIT("Progarchives"),
)
re_download = click.option(
    "-r",
    "--re-download",
    type=click.Choice(defaults.DL_CHOICES, case_sensitive=False),
    show_choices=True,
    default=defaults.DL_CHOICES[0],
    show_default=True,
    help="Re-download lists before merge.",
)


def add(func, decs: tuple):
    for dec in reversed(decs):
        func = dec(func)
    return func


def command(func, decs: tuple):
    return add(func, (count_time, version, debug, verbose, comm) + decs)


def aoty(func):
    return command(
        func, (aoty_lower, path.aoty("p"), text, path.aoty(text=True))
    )


def prog(func):
    return command(
        func, (prog_lower, path.prog("p"), text, path.prog(text=True))
    )


def dedup(func):
    return add(func, (deduplic, path.dedup))


def merge(func):
    return command(
        func, (
            re_download,
            dedup,
            path.merge("p"),
            text,
            path.merge(text=True),
            aoty_lower,
            prog_lower,
            path.aoty(),
            path.prog(),
        )
    )


def dirs(func):
    return command(
        func, (path.music, path.dirs("p"), text, path.dirs(text=True))
    )


def wanted(func):
    return command(
        func, (
            dedup,
            path.wanted("p"),
            text,
            path.wanted(text=True),
            path.merge(),
            path.dirs()
        )
    )


def leftover(func):
    return command(
        func, (
            dedup,
            path.leftover("p"),
            text,
            path.leftover(text=True),
            path.dirs(),
            path.merge()
        )
    )


def copy(func):
    return command(
        func, (path.music, path.destination, path.wanted(read=True))
    )
