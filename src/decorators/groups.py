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


cli_subgroup = cli.group(**group_args)


@cli_subgroup
def download() -> None:
    """Download lists of top albums from different music databases."""
    pass


@cli_subgroup
def duplicates() -> None:
    """Manage album duplicates between lists."""
    pass


@cli_subgroup
def transform() -> None:
    """Transform, merge and compare lists."""
    pass


transform_subgroup = transform.group(**group_args)


@transform_subgroup
def albums() -> None:
    """Transform, merge and compare lists of albums."""
    pass


@transform_subgroup
def tracks() -> None:
    """Transform, merge and compare lists of tracks."""
    pass


@cli_subgroup
def export() -> None:
    """Export album lists to other formats."""
    pass


@cli_subgroup
def files() -> None:
    """Get and manage album data from files."""
    pass
