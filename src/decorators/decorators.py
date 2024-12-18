#!/usr/bin/env python3

from functools import wraps
from time import time

import click
from click_help_colors import HelpColorsCommand, version_option

from src.decorators.groups import cli
from src.defaults import defaults
from src.defaults.click import CLICK_CONTEXT_SETTINGS


def count_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        print(f"Program concluded in {round(time() - start, 2)} seconds.")
        return result

    return wrapper


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
ceil = click.option(
    "-c/-f",
    "--ceil/--floor",
    is_flag=True,
    type=click.BOOL,
    default=defaults.CEIL,
    show_default=True,
    help="Round up (ceil) or down (floor) the score.",
)
use_dedup = click.option(
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
    "-H/-A",
    "--highest/--all-matches",
    is_flag=True,
    type=click.BOOL,
    default=True,
    show_default=True,
    help="Returns only the highest match of each entry, or every match.",
)
search = click.argument(
    "search",
    nargs=-1,
    required=False,
)
name = click.option(
    "-n",
    "--name",
    type=click.STRING,
    help="Use a personalized name instead of an auto-generated one.",
)


def __command__(name_: str | None = None):
    return cli.command(
        name=name_,
        context_settings=CLICK_CONTEXT_SETTINGS,
        cls=HelpColorsCommand,
    )


def __sub_command__(group: object, name_: str | None = None) -> object:
    return group.command(
        name=name_,
        context_settings=CLICK_CONTEXT_SETTINGS,
        cls=HelpColorsCommand,
    )


def __add_decorators__(func, decorators: tuple):
    for dec in reversed(decorators):
        func = dec(func)
    return func


def command(
    func: object,
    decorators: tuple,
    group: click.group = None,
    name_: str | None = None,
) -> object:
    return __add_decorators__(
        func,
        (
            version,
            debug,
            verbose,
            quiet,
            __sub_command__(group, name_) if group else __command__(name_),
        )
        + decorators
        + (count_time,),
    )
