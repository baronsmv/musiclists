#!/usr/bin/env python3

import click

from src.defaults import defaults


def HELP(name: str, maximum: bool = False):
    return f"""
        The {"maximum" if maximum else "minimum"} score threshold for {name}
        albums to be included in the list.
        The process will {"begin" if maximum else "stop"} once an album with a
        score {"equal to" if maximum else "lower than"} this threshold is
        encountered.
        """


def SCORE(
    name: str,
    score_type,
    default_score: int | float,
    letter: str | None = None,
    option: str | None = None,
    maximum: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    if no_name_option:
        option = str()
    else:
        option = (option if option else name[:4]).lower() + "-"
    option = "--" + option + ("max" if maximum else "min") + "-score"
    help_message = help_message if help_message else HELP(name)
    if letter:
        return click.option(
            "-" + letter,
            option,
            type=score_type,
            default=default_score,
            show_default=True,
            help=help_message,
        )
    else:
        return click.option(
            option,
            type=score_type,
            default=default_score,
            show_default=True,
            help=help_message,
        )


def aoty(
    name: str = "AOTY",
    score_type=click.INT,
    default_score: int | None = None,
    letter: str | None = None,
    option: str | None = None,
    maximum: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    if not default_score:
        default_score = (
            defaults.AOTY_MAX_SCORE if maximum else defaults.AOTY_MIN_SCORE
        )
    return SCORE(
        name=name,
        score_type=score_type,
        default_score=default_score,
        letter=letter,
        option=option,
        maximum=maximum,
        help_message=help_message,
        no_name_option=no_name_option,
    )


def prog(
    name: str = "Progarchives",
    score_type=click.FLOAT,
    default_score: float | None = None,
    letter: str | None = None,
    option: str | None = None,
    maximum: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    if not default_score:
        default_score = (
            defaults.PROG_MAX_SCORE if maximum else defaults.PROG_MIN_SCORE
        )
    return SCORE(
        name=name,
        score_type=score_type,
        default_score=default_score,
        letter=letter,
        option=option,
        maximum=maximum,
        help_message=help_message,
        no_name_option=no_name_option,
    )
