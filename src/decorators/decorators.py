#!/usr/bin/env python3

from functools import wraps
from time import time

import click
from click_help_colors import HelpColorsCommand, version_option

import src.defaults.click
from src.decorators import data, choice, groups, number, path
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
    help="Show only the highest match.",
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


def command(
    func: object, decorators: tuple, supercomm: object = None
) -> object:
    return add(
        func,
        (
            version,
            debug,
            verbose,
            quiet,
            subcomm(supercomm) if supercomm else comm,
        )
        + decorators
        + (count_time,),
    )


def aoty(func):
    return command(
        func,
        (
            choice.aoty(),
            number.aoty_score(letter="s"),
            number.aoty_score(letter="S", maximum=True),
            no_tracklist,
        ),
        groups.download,
    )


def prog(func):
    return command(
        func,
        (
            choice.prog(),
            number.prog_score(letter="s"),
            number.prog_score(letter="S", maximum=True),
            no_tracklist,
        ),
        groups.download,
    )


def duplicates(func):
    return command(
        func,
        (
            search,
            choice.columns(),
            data.source(suffix="1", default=0),
            data.source(suffix="2", default=1),
            highest_match,
            number.similarity(),
            number.num_results(),
        ),
        groups.search,
    )


def dedup(func):
    return add(func, (deduplic, path.dedup))


def merge(func):
    return command(
        func,
        (data.source(),),
        groups.operations,
    )


def albums(func):
    return command(
        func,
        (
            data.source(letter="d"),
            markdown,
            number.albums(letter="s"),
            number.albums(letter="S", maximum=True),
            number.ratings(letter="r"),
            number.ratings(letter="R", maximum=True),
        ),
        groups.output,
    )


def tracks(func):
    return command(
        func,
        (
            markdown,
            number.tracks(letter="s"),
            number.tracks(letter="S", maximum=True),
            number.albums(letter="a", show_name=True),
            number.albums(letter="A", show_name=True, maximum=True),
            number.ratings(letter="r"),
            number.ratings(letter="R", maximum=True),
        ),
        groups.output,
    )


def dirs(func):
    return command(
        func,
        (
            path.source,
            path.dirs(letter="p", no_name=True),
        ),
        groups.search,
    )


def wanted(func):
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


def leftover(func):
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


def copy(func):
    return command(
        func,
        (path.source, path.destination, path.wanted(read=True)),
        groups.operations,
    )
