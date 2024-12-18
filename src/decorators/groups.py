#!/usr/bin/env python3

from click import group
from click_help_colors import HelpColorsGroup

from src.defaults.click import (
    CLICK_CONTEXT_SETTINGS,
    HEADERS_COLOR,
    OPTIONS_COLOR,
)

group_args = dict(
    context_settings=CLICK_CONTEXT_SETTINGS,
    cls=HelpColorsGroup,
    help_headers_color=HEADERS_COLOR,
    help_options_color=OPTIONS_COLOR,
)

main_group = group(**group_args)


@main_group
def cli() -> None:
    """
    A command-line tool for downloading, filtering, and transforming top album
    and track lists from websites like AOTY.org and ProgArchives.com.
    """
    pass


cli_subgroup = cli.group(**group_args)


@cli_subgroup
def download() -> None:
    """Download lists of albums and tracks from music databases."""
    pass


@cli_subgroup
def duplicates() -> None:
    """Manage duplicated entries between lists."""
    pass


@cli_subgroup
def transform() -> None:
    """Transform, merge and compare lists."""
    pass


transform_subgroup = transform.group(**group_args)


@transform_subgroup
def albums() -> None:
    """Transform, operate and filter lists of albums."""
    pass


@transform_subgroup
def tracks() -> None:
    """Transform, operate and filter lists of tracks."""
    pass


@cli_subgroup
def export() -> None:
    """Export lists to other formats."""
    pass


@cli_subgroup
def files() -> None:
    """Get and manage albums and tracks data from files."""
    pass
