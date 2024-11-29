#!/usr/bin/env python3

import click
from click_help_colors import HelpColorsCommand, version_option
from functools import wraps
from time import time

from src.decorators import groups, path, score, types
from src.defaults import defaults


def count_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        print(f"Program concluded in {round(time() - start, 2)} seconds.")
        return result
    return wrapper


def subcomm(supercomm):
    return supercomm.command(
        cls=HelpColorsCommand,
    )


cli = groups.cli

comm = cli.command(
    cls=HelpColorsCommand,
)
version = version_option(
    version=defaults.VERSION,
    prog_name=defaults.PROG_NAME,
    message_color="green",
)
quiet = click.option(
    "-q",
    "--quiet",
    is_flag=True,
    type=click.BOOL,
    default=defaults.QUIET,
    show_default=True,
    help="Suppress messages. Only errors will be shown.",
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
    help="Omit tracklist and total length data, slightly speeding up the process.",
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
data_source = click.option(
    "-s",
    "--source",
    type=click.Choice(defaults.DATA_CHOICES.keys(), case_sensitive=False),
    show_choices=True,
    default=tuple(defaults.DL_CHOICES.keys())[0],
    show_default=True,
    help="Re-download lists before merge.",
)


def add(func, decs: tuple):
    for dec in reversed(decs):
        func = dec(func)
    return func


def command(func, decs: tuple, supercomm=None):
    return add(
        func,
        (
            count_time,
            version,
            debug,
            verbose,
            quiet,
            subcomm(supercomm) if supercomm else comm,
        )
        + decs,
    )


def aoty(func):
    return command(
        func,
        (
            types.aoty(letter="t", no_name_option=True),
            score.aoty(letter="m", no_name_option=True),
            score.aoty(letter="M", maximum=True, no_name_option=True),
            no_tracklist,
        ),
        groups.download,
    )


def prog(func):
    return command(
        func,
        (
            types.prog(letter="t", no_name_option=True),
            score.prog(letter="m", no_name_option=True),
            score.prog(letter="M", maximum=True, no_name_option=True),
            no_tracklist,
        ),
        groups.download,
    )


def dedup(func):
    return add(func, (deduplic, path.dedup))


def merge(func):
    return command(
        func,
        (
            dedup,
        ),
    )


def json(func):
    return command(
        func,
        (
            data_source,
        ),
    )


def dirs(func):
    return command(
        func, (
            path.source,
            path.dirs(letter="p", no_name_option=True),
        ),
    )


def wanted(func):
    return command(
        func,
        (
            path.wanted(letter="p", no_name_option=True),
            dedup,
            path.merge(read=True),
            path.dirs(read=True),
        ),
        groups.identify
    )


def leftover(func):
    return command(
        func,
        (
            path.leftover(letter="p", no_name_option=True),
            dedup,
            path.dirs(read=True),
            path.merge(read=True),
        ),
        groups.identify
    )


def copy(func):
    return command(
        func, (
            path.source,
            path.destination,
            path.wanted(read=True)
        )
    )
