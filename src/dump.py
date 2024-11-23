#!/usr/bin/env python3

from collections.abc import Iterator
from pathlib import Path
import re
from itertools import count
from subprocess import run, PIPE
from shlex import split as splitsh

from src.defaults import defaults, html_tags
from src import get
from src.error import pr as error
from src.verify import containsdirs, isdate
from src import search


def page(
    webpage: str,
    no_list: bool = False,
    list_only: bool = False,
    source: bool = False,
    encoding: str = "utf-8",
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> str:
    bashCommand = "lynx -dump -width=1000"
    bashCommand += " -source" if source else ""
    bashCommand += " -nolist" if no_list else " -listonly" if list_only else ""
    bashCommand += f" {webpage}"
    try:
        return run(
            splitsh(bashCommand),
            stdout=PIPE,
            encoding=encoding,
            errors="backslashreplace",
            check=True,
            text=True,
        ).stdout
    except Exception as err:
        error("webpage", [bashCommand], err)
    return str()


def until(
    function,
    type1: list | tuple,
    type2: list | tuple | int,
    min_score: int | float,
    include_url: bool = defaults.INCLUDE_URL,
    include_tracks: bool = defaults.INCLUDE_TRACKS,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator:
    for a in type1:
        foundLimit = False
        iterType = count(type2) if isinstance(type2, int) else iter(type2)
        while not foundLimit:
            b = next(iterType)
            for album in function(
                a,
                b,
                include_url=include_url,
                include_tracks=include_tracks,
                verbose=verbose,
                debug=debug,
            ):
                score = get.score(album)
                if score and score < min_score:
                    foundLimit = True
                    break
                else:
                    yield album


def aoty(
    albumType: str,
    pageNumber: int,
    include_url: bool = defaults.INCLUDE_URL,
    include_tracks: bool = defaults.INCLUDE_TRACKS,
    base_page: str = "https://www.albumoftheyear.org",
    ratings_subpage: str = "ratings/user-highest-rated",
    list_tags: dict = html_tags.aoty_albumlist,
    album_tags: dict = html_tags.aoty_album,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    if verbose:
        print(f"- Downloading {albumType}, page {pageNumber}...")
    pg = f"{base_page}/{ratings_subpage}/{albumType}/all/{pageNumber}/"
    albums_list = get.table(url=pg, id="centerContent")
    for data in albums_list.find_all(class_="albumListRow"):
        album = dict()  # type: dict[str, str | int | list]
        get.tag(element=data, data_struct=album, tags=list_tags)
        album_data = get.table(
            url=base_page + str(album["album_url"]), id="centerContent"
        )
        get.tag(element=album_data, data_struct=album, tags=album_tags)
        print(album)
        exit()


def prog_genres(
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator:
    pg = "https://www.progarchives.com/"
    data = page(pg, list_only=True)
    for lines in search.lines(r"subgenre\.asp\?style=", data):
        yield lines.group().split("=")[-1]


def prog_genre(
    pageNumber: int,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> str:
    pg = "https://www.progarchives.com/subgenre.asp"
    result = page(f"{pg}?style={pageNumber}", no_list=True)
    genre = re.search(".*Top Albums.*", result)
    if genre:
        return genre.group().replace(" Top Albums", "").strip()
    else:
        error("prog genre", [f"{pg}?style={pageNumber}"])
        return str()


def progarchives(
    pagenumber: int,
    albumType: int,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator:
    genre = prog_genre(pagenumber)
    if verbose:
        print(f"- Downloading {genre}, page {pagenumber}, type {albumType}...")
    basePage = "progarchives.com/top-prog-albums.asp"
    pg = (
        basePage
        + f"?ssubgenres={pagenumber}"
        + f"&salbumtypes={albumType}"
        + "&smaxresults=250#list"
    )
    result = page(pg, no_list=True)
    for data in search.lines("QWR = ", result, before=2, after=3):
        try:
            lines = data.group().splitlines()
            position = int(lines[0].split("[", 1)[0])
            rating, ratings = (
                lines[1].replace(" ratings", "", 1).strip().split(" | ", 1)
            )
            rating = float(rating)
            ratings = int(ratings)
            score = float(lines[2].split(" = ")[1])
            title = lines[3].replace("/", "_").strip()
            artist = lines[4].replace(genre, "", 1).replace("/", "_").strip()
            releaseType, year = (
                lines[5].replace(" Shop", "", 1).strip().split(", ", 1)
            )
            year = int(year)
        except Exception as err:
            error("", lines, err)
        yield {
            get.id((artist, year, title)): {
                "artist": artist,
                "title": title,
                "year": year,
                "genre": genre,
                "score": score,
                "rating": rating,
                "ratings": ratings,
                "type": releaseType,
                "position": position,
                "page": pagenumber,
            }
        }


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
