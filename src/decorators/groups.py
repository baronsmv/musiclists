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
