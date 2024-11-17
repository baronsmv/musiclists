#!/usr/bin/env python3

import click
from click_help_colors import HelpColorsGroup

from src.defaults import defaults


@click.group(
    cls=HelpColorsGroup,
    help_headers_color=defaults.HEADERS_COLOR,
    help_options_color=defaults.OPTIONS_COLOR,
)
def cli() -> None:
    pass


@cli.group(
    cls=HelpColorsGroup,
    help_headers_color=defaults.HEADERS_COLOR,
    help_options_color=defaults.OPTIONS_COLOR,
)
def download() -> None:
    pass


@cli.group(
    cls=HelpColorsGroup,
    help_headers_color=defaults.HEADERS_COLOR,
    help_options_color=defaults.OPTIONS_COLOR,
)
def identify() -> None:
    pass
