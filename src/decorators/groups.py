#!/usr/bin/env python3

import click
from click_help_colors import HelpColorsGroup

import src.defaults.click

main_group = click.group(
    context_settings=src.defaults.click.CLICK_CONTEXT_SETTINGS,
    cls=HelpColorsGroup,
    help_headers_color=src.defaults.click.HEADERS_COLOR,
    help_options_color=src.defaults.click.OPTIONS_COLOR,
)


@main_group
def cli() -> None:
    """
    A command-line tool for downloading, merging, and analyzing top album lists
    from websites like AOTY.org and ProgArchives.com.

    Features:

        - Download lists of the top albums from multiple platforms such as
            AOTY.org and ProgArchives.com.

        - Provide utilities for merging, subtracting, filtering, sorting,
            and processing the album data, as well as their tracks.

        - Export to multiple formats, for further analysis.

    The tool helps you easily aggregate and explore curated album and track
    rankings across different platforms, making it ideal for music enthusiasts
    and data-driven listeners.
    """
    pass


sub_group = cli.group(
    context_settings=src.defaults.click.CLICK_CONTEXT_SETTINGS,
    cls=HelpColorsGroup,
    help_headers_color=src.defaults.click.HEADERS_COLOR,
    help_options_color=src.defaults.click.OPTIONS_COLOR,
)


@sub_group
def download() -> None:
    """Download lists of top albums from different music databases."""
    pass


@sub_group
def duplicates() -> None:
    """Manage album duplicates."""
    pass


@sub_group
def transform() -> None:
    """Transform, merge and compare album lists."""
    pass


@sub_group
def export() -> None:
    """Export album lists to other formats."""
    pass
