#!/usr/bin/env python3

from collections.abc import Iterator
from datetime import timedelta
from pathlib import Path
from itertools import count

from src.defaults import defaults
from src import get
from src.html_tags import aoty as aoty_tags, prog as prog_tags
from src.verify import containsdirs


def until(
    function,
    type1: list | tuple,
    type2: list | tuple | int,
    score_key: str,
    min_score: int | float,
    max_score: int | float,
    lowest_score: int | float = 0,
    highest_score: int | float = 100,
    no_tracklist: bool = defaults.NO_TRACKLIST,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator[dict[str, str | int | float | list | dict | timedelta]]:
    for a in type1:
        foundLimit = False
        iterType = count(type2) if isinstance(type2, int) else iter(type2)
        while not foundLimit:
            b = next(iterType)
            for album in function(
                a,
                b,
                quiet=quiet,
                verbose=verbose,
                debug=debug,
            ):
                score = album.get(score_key)
                if not score:
                    print(f"ERROR: Score not found for: {album}")
                    exit(1)
                if score < min_score:
                    foundLimit = True
                    break
                if min_score <= score <= max_score:
                    if verbose:
                        print(
                            "  - "
                            + (
                                f"{score:.4f}"
                                if isinstance(score, float)
                                else f"{score}"
                            )
                            + ": "
                            + get.path(album, sep=" - ")
                        )
                    album["id"] = get.id(album)
                    yield album


def aoty(
    album_type: str,
    page_number: int,
    base_page: str = "https://www.albumoftheyear.org",
    ratings_subpage: str = "ratings/user-highest-rated",
    list_tags: dict = aoty_tags.albumlist,
    album_tags: dict = aoty_tags.album,
    no_tracklist: bool = defaults.NO_TRACKLIST,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator[dict[str, str | int | float | list | dict | timedelta]]:
    if not quiet:
        print(f"- Downloading {album_type}, page {page_number}...")
    album = dict(
    )  # type: dict[str, str | int | float | list | dict | timedelta]
    url = f"{base_page}/{ratings_subpage}/{album_type}/all/{page_number}/"
    albums_list = get.table(url=url, id="centerContent")
    for data in albums_list.find_all(class_="albumListRow"):
        album["type"] = album_type
        album["page_number"] = page_number
        get.tag(element=data, data_struct=album, tags=list_tags)
        album_url = base_page + str(album["album_url"])
        album["internal_id"] = int(
            album_url.split("album/", 1)[-1].split("-", 1)[0]
        )
        album_data = get.table(url=album_url, id="centerContent")
        get.tag(element=album_data, data_struct=album, tags=album_tags)
        if not no_tracklist:
            album["tracks"], album["total_length"] = get.aoty_tracks(album_url)
        yield album.copy()
        album.clear()


def progarchives(
    genre: tuple,
    album_type: int,
    base_page: str = "https://www.progarchives.com/",
    list_tags: dict = prog_tags.albumlist,
    album_tags: dict = prog_tags.album,
    no_tracklist: bool = defaults.NO_TRACKLIST,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator[dict[str, str | int | float | list | dict | timedelta]]:
    if not quiet:
        print(
            f"- Downloading {genre[0]}, page {genre[1]}, type {album_type}..."
        )
    album = dict(
    )  # type: dict[str, str | int | float | list | dict | timedelta]
    url = (
        base_page
        + "top-prog-albums.asp"
        + f"?ssubgenres={genre[1]}"
        + f"&salbumtypes={album_type}"
        + "&smaxresults=250#list"
    )
    albums_list = get.table(url=url, tag="table", number=1, encoding="latin1")
    for data in albums_list.find_all("tr"):
        album["type"] = album_type
        album["genre"] = genre[0]
        get.tag(element=data, data_struct=album, tags=list_tags)
        album_url = base_page + str(album["album_url"])
        album["internal_id"] = int(album_url.split("?id=")[-1])
        album_data = get.table(url=album_url, tag="td", encoding="latin1")
        get.tag(element=album_data, data_struct=album, tags=album_tags)
        album["score_distribution"] = get.prog_distribution_score(album_url)
        if not no_tracklist:
            album["tracks"], album["total_length"] = get.prog_tracks(album_url)
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
            and not containsdirs(d)
            and min_level <= get.level(d, path) <= max_level
        ):
            yield d
