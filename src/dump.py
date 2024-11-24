#!/usr/bin/env python3

from collections.abc import Iterator
from pathlib import Path
import re
from itertools import count

from src.defaults import defaults
from src import get
from src.html_tags import aoty as aoty_tags, prog as prog_tags
from src.error import pr as error
from src.verify import containsdirs, isdate
from src import search


def until(
    function,
    type1: list | tuple,
    type2: list | tuple | int,
    min_score: int | float,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator[dict[str, str | int | float | list]]:
    for a in type1:
        foundLimit = False
        iterType = count(type2) if isinstance(type2, int) else iter(type2)
        while not foundLimit:
            b = next(iterType)
            for album in function(
                a,
                b,
                verbose=verbose,
                debug=debug,
            ):
                score = album.get("user_score")
                if score and score < min_score:
                    foundLimit = True
                    break
                elif not score:
                    print(f"ERROR: Score not found: {album}")
                    exit(1)
                else:
                    yield album


def aoty(
    album_type: str,
    page_number: int,
    base_page: str = "https://www.albumoftheyear.org",
    ratings_subpage: str = "ratings/user-highest-rated",
    list_tags: dict = aoty_tags.albumlist,
    album_tags: dict = aoty_tags.album,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator[dict[str, str | int | float | list]]:
    if verbose:
        print(f"- Downloading {album_type}, page {page_number}...")
    url = f"{base_page}/{ratings_subpage}/{album_type}/all/{page_number}/"
    albums_list = get.table(url=url, id="centerContent")
    for data in albums_list.find_all(class_="albumListRow"):
        album = dict()  # type: dict[str, str | int | float | list]
        album["type"] = album_type
        album["page_number"] = page_number
        get.tag(element=data, data_struct=album, tags=list_tags)
        album_url = base_page + str(album["album_url"])
        if debug:
            print(album_url)
        album_data = get.table(url=album_url, id="centerContent")
        get.tag(element=album_data, data_struct=album, tags=album_tags)
        album["tracks"] = get.aoty_tracks(album_url)
        if debug:
            print(album, end="\n\n")
        yield album.copy()
        album.clear()


def progarchives(
    genre: tuple,
    album_type: int,
    base_page: str = "https://www.progarchives.com/top-prog-albums.asp",
    list_tags: dict = prog_tags.albumlist,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator:
    if verbose:
        print(
            f"- Downloading {genre[0]}, page {genre[1]}, type {album_type}..."
        )
    url = (
        base_page
        + f"?ssubgenres={genre[1]}"
        + f"&salbumtypes={album_type}"
        + "&smaxresults=250#list"
    )
    albums_list = get.table(url=url, tag="table", number=1, encoding="latin1")
    for data in albums_list.find_all("tr"):
        print(data)
        album = dict()  # type: dict[str, str | int | float | list]
        album["type"] = album_type
        album["genre"] = genre[0]
        get.tag(element=data, data_struct=album, tags=list_tags)
        print(album)
        exit()
        album_url = base_page + str(album["album_url"])
        if debug:
            print(album_url)
        album_data = get.table(url=album_url, id="centerContent")
        get.tag(element=album_data, data_struct=album, tags=album_tags)
        album["tracks"] = get.aoty_tracks(album_url)
        if debug:
            print(album, end="\n\n")
        yield album.copy()
        album.clear()


def dirs(
    path: Path,
    minLevel: int = defaults.MIN_LEVEL,
    maxLevel: int = defaults.MAX_LEVEL,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator[Path]:
    for d in path.rglob("*"):
        if (
            d.is_dir()
            and not containsdirs(d)
            and minLevel <= get.level(d, path) <= maxLevel
        ):
            yield d
