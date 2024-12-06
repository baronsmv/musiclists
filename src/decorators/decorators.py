#!/usr/bin/env python3

from functools import wraps
from time import time

import click
from click_help_colors import HelpColorsCommand, version_option

import src.defaults.click
from src.decorators import groups
from src.defaults import defaults


def count_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        print(f"Program concluded in {round(time() - start, 2)} seconds.")
        return result

    return wrapper


def subcomm(supercomm: object) -> object:
    return supercomm.command(
        context_settings=src.defaults.click.CLICK_CONTEXT_SETTINGS,
        cls=HelpColorsCommand,
    )


cli = groups.cli

comm = cli.command(
    context_settings=src.defaults.click.CLICK_CONTEXT_SETTINGS,
    cls=HelpColorsCommand,
)
version = version_option(
    version=defaults.VERSION,
    prog_name=defaults.APP_NAME,
    message_color="green",
)
quiet = click.option(
    "-q",
    "--quiet",
    is_flag=True,
    type=click.BOOL,
    default=defaults.QUIET,
    show_default=True,
    help="Suppress console output. Only warnings and errors will be displayed.",
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
no_tracklist = click.option(
    "-n",
    "--no-tracklist",
    is_flag=True,
    type=click.BOOL,
    default=defaults.NO_TRACKLIST,
    show_default=True,
    help="Tracklist and total length data information will not be retrieved, "
    + "slightly speeding up the process.",
)
dedup = click.option(
    "-d",
    "--dedup/--no-dedup",
    is_flag=True,
    type=click.BOOL,
    default=True,
    show_default=True,
    help="Deduplicate the output based on its deduplicates file.",
)
markdown = click.option(
    "-m",
    "--markdown/--no-markdown",
    is_flag=True,
    type=click.BOOL,
    default=True,
    show_default=True,
    help="Output as MarkDown.",
)
highest_match = click.option(
    "-h",
    "--highest/--all-matches",
    is_flag=True,
    type=click.BOOL,
    default=True,
    show_default=True,
    help="Returns only the highest match of each entry.",
)
search = click.argument(
    "search",
    nargs=-1,
    required=False,
)


def add(func, decorators: tuple):
    for dec in reversed(decorators):
        func = dec(func)
    return func


def command(func: object, decorators: tuple, group: object = None) -> object:
    return add(
        func,
        (
            version,
            debug,
            verbose,
            quiet,
            subcomm(group) if group else comm,
        )
        + decorators
        + (count_time,),
    )


def dirs(func):
    """
    return command(
        func,
        (
            path.source,
            path.dirs(letter="p", no_name=True),
        ),
        groups.search,
    )
    """


def wanted(func):
    """
    return command(
        func,
        (
            path.wanted(letter="p", no_name=True),
            dedup,
            path.merge(read=True),
            path.dirs(read=True),
        ),
        groups.search,
    )
    """


def leftover(func):
    """
    return command(
        func,
        (
            path.leftover(letter="p", no_name=True),
            dedup,
            path.dirs(read=True),
            path.merge(read=True),
        ),
        groups.search,
    )
    """


def copy(func):
    """
    return command(
        func,
        (path.source, path.destination, path.wanted(read=True)),
        groups.operations,
    )
    """
