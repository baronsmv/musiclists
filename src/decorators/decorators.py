#!/usr/bin/env python3

import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand, version_option
from functools import wraps
from time import time

from src.decorators import path
from src.defaults import defaults as default


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


def SAVE(name: str, suffix: str, direction: str) -> str:
    return f"Path to save {name} {suffix} file {direction}."


def LOWER_LIMIT(name: str):
    return f"Lower limit for {name} score."


comm = cli.command(
    cls=HelpColorsCommand,
)
version = version_option(
    version=default.VERSION,
    prog_name=default.PROG_NAME,
    message_color="green"
)
verbose = click.option(
    "-v",
    "--verbose",
    is_flag=True,
    type=click.BOOL,
    help="Show information of process.",
)
text = click.option(
    "-t",
    "--text",
    is_flag=True,
    type=click.BOOL,
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
    default=default.AOTY_SCORE,
    show_default=True,
    help=LOWER_LIMIT("AOTY"),
)
prog_lower = click.option(
    "--prog-lower",
    type=click.FLOAT,
    default=default.PROG_SCORE,
    show_default=True,
    help=LOWER_LIMIT("Progarchives"),
)
re_download = click.option(
    "-r",
    "--re-download",
    type=click.Choice(default.DL_CHOICES, case_sensitive=False),
    show_choices=True,
    default=default.DL_CHOICES[0],
    show_default=True,
    help="Re-download lists before merge.",
)


def add(func, decorators: tuple):
    for dec in decorators:
        func = dec(func)
    return func


def new_command(func):
    return add(func, (comm, verbose, version))


def aoty(func):
    return add(func, (path.aoty(text=True), text, path.aoty, aoty_lower))


def prog(func):
    return add(func, (path.prog(text=True), text, path.prog, prog_lower))


def dedup(func):
    return add(func, (path.dedup, deduplic))


def merge(func):
    return add(func, (path.merge(text=True), text, path.merge, re_download))


def dirs(func):
    return add(func, (path.dirs(text=True), text, path.dirs))


def wanted(func):
    return add(func, (path.wanted(text=True), text, path.leftover))


def leftover(func):
    return add(func, (path.leftover(text=True), text, path.leftover))
