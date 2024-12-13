#!/usr/bin/env python3

import math
import pprint
from collections.abc import Iterator
from datetime import timedelta
from itertools import count
from pathlib import Path

from src.attributes import aoty as aoty_tags, prog as prog_tags
from src.classes.Album import Album
from src.debug import logging
from src.defaults import defaults
from src.get import data as get_data, file as get_file
from src.get.file import contains_dirs


def until(
    function,
    type1: list | tuple,
    type2: list | tuple | int,
    score_key: str,
    min_score: int | float,
    max_score: int | float,
    ceil: bool = defaults.CEIL,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator[dict[str, str | int | float | list | dict | timedelta]]:
    logger = logging.logger(until)
    for a in type1:
        found_limit = False
        iter_type = count(type2) if isinstance(type2, int) else iter(type2)
        while not found_limit:
            b = next(iter_type)
            for album in function(
                a,
                b,
                ceil=ceil,
                quiet=quiet,
                verbose=verbose,
                debug=debug,
            ):
                album = Album(album)
                album.compute_id()
                score = album.get(score_key)
                if not score:
                    logger.error(
                        f"Score with key {score_key}, not found for:\n{album}"
                    )
                    exit(1)
                if score < min_score:
                    if debug:
                        logger.info(
                            f"Found lower score ({score}) than limit for:\n{album}"
                        )
                    found_limit = True
                    break
                if min_score <= score <= max_score:
                    if verbose:
                        print(f"   {score}: {album}")
                    yield dict(album)


def aoty(
    album_type: str,
    page_number: int,
    base_page: str = "https://www.albumoftheyear.org",
    ratings_subpage: str = "ratings/user-highest-rated",
    list_tags: dict = aoty_tags.album_list,
    album_tags: dict = aoty_tags.album,
    ceil: bool = defaults.CEIL,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator[Album]:
    logger = logging.logger(aoty)
    message = f"- Downloading {album_type}, page {page_number}..."
    if debug:
        logger.info(message + f", ceil = {ceil}")
    if not quiet:
        print(message)
    album = Album()
    url = f"{base_page}/{ratings_subpage}/{album_type}/all/{page_number}/"
    if debug:
        logger.debug(f"URL is {url}")
    albums_list = get_data.table(
        url=url,
        id="centerContent",
        debug=debug,
    )
    for data in albums_list.find_all(class_="albumListRow"):
        album["internal_id"] = -1
        album["type"] = album_type
        album["page_number"] = page_number
        get_data.data(element=data, data_struct=album, tags=list_tags)
        album_url = base_page + str(album["album_url"])
        album["internal_id"] = int(
            tuple(album_url.split("album/", 1))[-1].split("-", 1)[0]
        )
        album_data = get_data.table(
            url=album_url, id="centerContent", debug=debug
        )
        get_data.data(element=album_data, data_struct=album, tags=album_tags)
        album["tracks"], album["total_length"] = get_data.aoty_tracks(
            url=album_url,
            debug=debug,
        )
        if not album["total_length"]:
            del album["total_length"]
        if debug:
            logger.debug(pprint.pformat(album))
        yield album.copy()
        album.clear()


def prog(
    genre: tuple[str, int],
    album_type: tuple[str, int],
    base_page: str = "https://www.progarchives.com/",
    list_tags: dict = prog_tags.album_list,
    album_tags: dict = prog_tags.album,
    ceil: bool = defaults.CEIL,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator[Album]:
    logger = logging.logger(prog)
    message = f"- Downloading {genre[0]}, type {album_type[0]}..."
    if debug:
        logger.info(message + f", ceil = {ceil}")
    if not quiet:
        print(message)
    album = Album()
    url = (
        base_page
        + "top-prog-albums.asp"
        + f"?ssubgenres={genre[1]}"
        + f"&salbumtypes={album_type[1]}"
        + "&smaxresults=250#list"
    )
    if debug:
        logger.debug(f"URL is {url}")
    albums_list = get_data.table(
        url=url, tag="table", number=1, encoding="latin1"
    )
    for data in albums_list.find_all("tr"):
        album["type"] = album_type[0]
        album["genre"] = genre[0]
        get_data.data(element=data, data_struct=album, tags=list_tags)
        album_url = base_page + str(album["album_url"])
        album["internal_id"] = int(tuple(album_url.split("?id="))[-1])
        album_data = get_data.table(url=album_url, tag="td", encoding="latin1")
        get_data.data(element=album_data, data_struct=album, tags=album_tags)
        album["user_score"] = (math.ceil if ceil else math.floor)(
            album["qwr"] * 20
        )
        album["score_distribution"] = get_data.prog_distribution_score(
            album_url
        )
        album["tracks"], album["total_length"] = get_data.prog_tracks(
            album_url
        )
        if debug:
            logger.debug(pprint.pformat(album))
        yield album.copy()
        album.clear()


def dirs(
    path: Path,
    min_level: int = defaults.MIN_LEVEL,
    max_level: int = defaults.MAX_LEVEL,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator[Path]:
    for d in path.rglob("*"):
        if (
            d.is_dir()
            and not contains_dirs(d)
            and min_level <= get_file.level(d, path) <= max_level
        ):
            yield d
