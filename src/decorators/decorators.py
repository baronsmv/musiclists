#!/usr/bin/env python3

import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand, version_option
from functools import wraps
from time import time

from src.decorators import path, score
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
        func, (
            score.aoty(letter="m", no_name_option=True),
            path.aoty(letter="p", no_name_option=True),
            text,
            path.aoty(text=True, no_name_option=True)
        )
    )


def prog(func):
    return command(
        func, (
            score.prog(letter="m", no_name_option=True),
            path.prog(letter="p", no_name_option=True),
            text,
            path.prog(text=True, no_name_option=True)
        )
    )


def dedup(func):
    return add(func, (deduplic, path.dedup))


def merge(func):
    return command(
        func, (
            re_download,
            dedup,
            path.merge(letter="p", no_name_option=True),
            text,
            path.merge(text=True, no_name_option=True),
            score.aoty(),
            score.prog(),
            path.aoty(),
            path.prog(),
        )
    )


def dirs(func):
    return command(
        func, (path.music, path.dirs(letter="p"), text, path.dirs(text=True))
    )


def wanted(func):
    return command(
        func, (
            dedup,
            path.wanted(letter="p", no_name_option=True),
            text,
            path.wanted(text=True, no_name_option=True),
            path.merge(read=True),
            path.dirs(read=True)
        )
    )


def leftover(func):
    return command(
        func, (
            dedup,
            path.leftover(letter="p", no_name_option=True),
            text,
            path.leftover(text=True, no_name_option=True),
            path.dirs(read=True),
            path.merge(read=True)
        )
    )


def copy(func):
    return command(
        func, (
            path.music,
            path.destination,
            path.wanted(read=True)
        )
    )
