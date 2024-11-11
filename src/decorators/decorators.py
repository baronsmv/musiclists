#!/usr/bin/env python3

import click
from click_help_colors import HelpColorsGroup, HelpColorsCommand, version_option
from functools import wraps
from pathlib import Path
from time import time

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


FILE = click.Path(
    exists=False, dir_okay=False, writable=True, path_type=Path,
)
DIR = click.Path(
    exists=True, dir_okay=True, path_type=Path,
)


group = click.group(
    cls=HelpColorsGroup,
    help_headers_color="yellow",
    help_options_color="green",
)

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
text_dir = click.option(
    "--text-dir",
    type=DIR,
    default=default.TXT_DIR,
    show_default=True,
    help="Directory of text file.",
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
dedup_dir = click.option(
    "--dedup-dir",
    type=DIR,
    default=default.DEDUP_DIR,
    show_default=True,
    help="Directory of deduplicates files.",
)
aoty_path = click.option(
    "--aoty-path",
    type=FILE,
    default=default.AOTY_PATH,
    show_default=True,
    help="Path to save AOTY list.",
)
aoty_lower = click.option(
    "--aoty-lower",
    type=click.INT,
    default=default.AOTY_SCORE,
    show_default=True,
    help="Lower limit for AOTY score.",
)
prog_path = click.option(
    "--prog-path",
    type=FILE,
    default=default.PROG_PATH,
    show_default=True,
    help="Path to save Progarchives list.",
)
prog_lower = click.option(
    "--prog-lower",
    type=click.FLOAT,
    default=default.PROG_SCORE,
    show_default=True,
    help="Lower limit for Progarchives score.",
)
merge_path = click.option(
    "--merge-path",
    type=FILE,
    default=default.MERGE_PATH,
    show_default=True,
    help="Path to save merged list.",
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
music_path = click.argument(
    "music_path",
    type=DIR,
)
dirs_path = click.option(
    "--dirs-path",
    type=FILE,
    default=default.DIRS_PATH,
    show_default=True,
    help="Path to save list.",
)
wanted_path = click.option(
    "--wanted-path",
    type=FILE,
    default=default.WANTED_PATH,
    show_default=True,
    help="Path to save list.",
)
leftover_path = click.option(
    "--left-path",
    type=FILE,
    default=default.LEFTOVER_PATH,
    show_default=True,
    help="Path to save list.",
)
destination_path = click.argument(
    "destination_path",
    type=DIR,
)


def add(func, decorators):
    for dec in decorators:
        func = dec(func)
    return func


def new_command(func):
    return add(func, (comm, verbose, version))


def new_list(func):
    return add(func, (comm, text, text_dir, verbose, version))


def aoty(func):
    return add(func, (aoty_path, aoty_lower))


def prog(func):
    return add(func, (prog_path, prog_lower))


def dedup(func):
    return add(func, (dedup_dir, deduplic))
