#!/usr/bin/env python3

import click
from click_help_colors import HelpColorsGroup

from src.defaults import defaults

main_group = click.group(
    cls=HelpColorsGroup,
    help_headers_color=defaults.HEADERS_COLOR,
    help_options_color=defaults.OPTIONS_COLOR,
)


@main_group
def cli() -> None:
    """
    A command-line tool for downloading, merging, and analyzing top album lists
    from websites like AOTY.org and ProgArchives.com.

    Features:

        - Download lists of the top albums from multiple platforms such as
            AOTY.org and Progarchives.com.

        - Merge these lists into a single JSON file for further analysis.

        - Provide utilities for filtering, sorting, and processing the album
            data.

        - Analyze the album data to derive useful insights, trends and
            comparisons.

    The tool helps you easily aggregate and explore curated album rankings
    across different platforms, making it ideal for music enthusiasts and
    data-driven listeners.
    """
    pass


sub_group = cli.group(
    cls=HelpColorsGroup,
    help_headers_color=defaults.HEADERS_COLOR,
    help_options_color=defaults.OPTIONS_COLOR,
)


@sub_group
def download() -> None:
    pass


@sub_group
def identify() -> None:
    pass
