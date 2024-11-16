#!/usr/bin/env python3

from collections.abc import Iterator
from pathlib import Path
import re
from itertools import count
from subprocess import run, PIPE
from shlex import split as splitsh

from src.defaults import defaults
from src import get
from src.error import pr as error
from src.verify import containsdirs, isdate
from src import search


def page(webpage: str, listonly: bool = False) -> str:
    bashCommand = "lynx -dump -width=1000 "
    bashCommand += "-listonly" if listonly else "-nolist"
    bashCommand += f" {webpage}"
    try:
        return run(
            splitsh(bashCommand),
            stdout=PIPE,
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
    lowerlimit: int | float,
    verbose: bool = defaults.VERBOSE,
) -> Iterator:
    for a in type1:
        foundLimit = False
        iterType = count(type2) if isinstance(type2, int) else iter(type2)
        while not foundLimit:
            b = next(iterType)
            for album in function(a, b, verbose=verbose):
                score = get.score(album)
                if score and score < lowerlimit:
                    foundLimit = True
                    break
                else:
                    yield album


def aoty(
    albumType: str,
    pageNumber: int,
    verbose: bool = defaults.VERBOSE,
) -> Iterator:
    if verbose:
        print(f"- Downloading {albumType}, page {pageNumber}...")
    basePage = "albumoftheyear.org/ratings/user-highest-rated"
    pg = f"{basePage}/{albumType}/all/{pageNumber}/"
    result = page(pg)
    for data in search.lines(r"\d\. ", result, 0, 7):
        base = 0
        lines = data.group().splitlines()
        try:
            line = lines[base + 0].strip().split(". ", 1)
            position = int(line[0])
            artist, title = line[1].replace("/", "_").split(" - ", 1)
            if not isdate(lines[base + 3].strip()):
                base = base - 1
            year = int(lines[base + 3][-4:])
            if "USER SCORE" in lines[base + 4]:
                base = base - 1
                genre = ["Unknown"]
            else:
                genre = lines[base + 4].strip().split(", ")
            score = int(lines[base + 6].strip())
            ratings = int(
                lines[base + 7].strip().split(" ")[0].replace(",", "")
            )
        except Exception as err:
            error("", lines, err)
        yield {
            get.id((artist, year, title)): {
                "artist": artist,
                "title": title,
                "year": year,
                "genre": genre,
                "score": score,
                "ratings": ratings,
                "type": albumType,
                "position": position,
                "page": pageNumber,
            }
        }


def proggenres() -> Iterator:
    pg = "https://www.progarchives.com/"
    data = page(pg, listonly=True)
    for lines in search.lines(r"subgenre\.asp\?style=", data):
        yield lines.group().split("=")[-1]


def proggenre(pageNumber: int) -> str:
    pg = "https://www.progarchives.com/subgenre.asp"
    result = page(f"{pg}?style={pageNumber}")
    genre = re.search(".*Top Albums.*", result)
    if genre:
        return genre.group().replace(" Top Albums", "").strip()
    else:
        error("prog genre", [f"{pg}?style={pageNumber}"])
        return str()


def progarchives(
    pagenumber: int, albumType: int, verbose: bool = defaults.VERBOSE
) -> Iterator:
    genre = proggenre(pagenumber)
    if verbose:
        print(f"- Downloading {genre}, page {pagenumber}, type {albumType}...")
    basePage = "progarchives.com/top-prog-albums.asp"
    pg = (
        basePage
        + f"?ssubgenres={pagenumber}"
        + f"&salbumtypes={albumType}"
        + "&smaxresults=250#list"
    )
    result = page(pg)
    for data in search.lines("QWR = ", result, 2, 3):
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
) -> Iterator[Path]:
    for d in path.rglob("*"):
        if (
            d.is_dir()
            and not containsdirs(d)
            and minLevel <= get.level(d, path) <= maxLevel
        ):
            yield d
