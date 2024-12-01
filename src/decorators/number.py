#!/usr/bin/env python3

import click

import src.defaults.download
from src.defaults import defaults


def __help__(
    name: str | None,
    maximum: bool = False,
    elements: str | None = "albums",
    no_score: bool = False,
):
    name = "" if not name else name
    return f"""
        {"Maximum" if maximum else "Minimum"}
        {name if no_score else "score threshold"}
        for including {
            ("" if no_score else name)
            + (" " if elements and not no_score else "")
            + (elements if elements else "")
        }.
        """


def __number__(
    name: str | None,
    default_score: int | float | None = None,
    integer: bool = True,
    letter: str | None = None,
    option: str | None = None,
    maximum: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
    elements: str | None = "albums",
    no_score: bool = False,
):
    if no_name_option or not name:
        option = str()
    else:
        option = "-" + (option if option else name[:4]).lower()
    option = "--" + ("max" if maximum else "min") + option
    if not no_score:
        option = option + "-score"
    help_message = (
        help_message
        if help_message
        else __help__(
            name=name,
            maximum=maximum,
            elements=elements,
            no_score=no_score,
        )
    )
    if letter:
        return click.option(
            "-" + letter,
            option,
            type=click.INT if integer else click.FLOAT,
            default=default_score,
            show_default=True,
            help=help_message,
        )
    else:
        return click.option(
            option,
            type=click.INT if integer else click.FLOAT,
            default=default_score,
            show_default=True,
            help=help_message,
        )


def aoty(
    name: str | None = "AOTY",
    integer: bool = True,
    default_score: int | None = None,
    letter: str | None = None,
    option: str | None = None,
    maximum: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    if not default_score:
        default_score = (
            src.defaults.download.AOTY_MAX_SCORE
            if maximum
            else src.defaults.download.AOTY_MIN_SCORE
        )
    return __number__(
        name=name,
        integer=integer,
        default_score=default_score,
        letter=letter,
        option=option,
        maximum=maximum,
        help_message=help_message,
        no_name_option=no_name_option,
    )


def prog(
    name: str | None = "Progarchives",
    integer: bool = False,
    default_score: float | None = None,
    letter: str | None = None,
    option: str | None = None,
    maximum: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    if not default_score:
        default_score = (
            src.defaults.download.PROG_MAX_SCORE
            if maximum
            else src.defaults.download.PROG_MIN_SCORE
        )
    return __number__(
        name=name,
        integer=integer,
        default_score=default_score,
        letter=letter,
        option=option,
        maximum=maximum,
        help_message=help_message,
        no_name_option=no_name_option,
    )


def albums(
    name: str | None = "albums",
    integer: bool = True,
    default_score: int | None = None,
    letter: str | None = None,
    option: str | None = "album",
    maximum: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    if not default_score:
        default_score = (
            defaults.ALBUM_MAX_SCORE if maximum else defaults.ALBUM_MIN_SCORE
        )
    return __number__(
        name=name,
        integer=integer,
        default_score=default_score,
        letter=letter,
        option=option,
        maximum=maximum,
        help_message=help_message,
        no_name_option=no_name_option,
        elements="",
    )


def tracks(
    name: str | None = "tracks",
    integer: bool = True,
    default_score: int | None = None,
    letter: str | None = None,
    option: str | None = "tracks",
    maximum: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    if not default_score:
        default_score = (
            defaults.TRACK_MAX_SCORE if maximum else defaults.TRACK_MIN_SCORE
        )
    return __number__(
        name=name,
        integer=integer,
        default_score=default_score,
        letter=letter,
        option=option,
        maximum=maximum,
        help_message=help_message,
        no_name_option=no_name_option,
        elements=None,
    )


def ratings(
    name: str | None = "ratings",
    integer: bool = True,
    default_score: int | None = None,
    letter: str | None = None,
    option: str | None = "ratings",
    maximum: bool = False,
    help_message: str | None = None,
    no_name_option: bool = False,
):
    if not default_score:
        default_score = (
            defaults.MAX_RATINGS if maximum else defaults.MIN_RATINGS
        )
    return __number__(
        name=name,
        integer=integer,
        default_score=default_score,
        letter=letter,
        option=option,
        maximum=maximum,
        help_message=help_message,
        no_name_option=no_name_option,
        no_score=True,
        elements="tracks",
    )
