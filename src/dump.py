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


def page(
    webpage: str,
    no_list: bool = False,
    list_only: bool = False,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> str:
    bashCommand = "lynx -dump -width=1000"
    bashCommand += " -nolist" if no_list else " -listonly" if list_only else ""
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
    debug: bool = defaults.DEBUG,
) -> Iterator:
    for a in type1:
        foundLimit = False
        iterType = count(type2) if isinstance(type2, int) else iter(type2)
        while not foundLimit:
            b = next(iterType)
            for album in function(a, b, verbose=verbose, debug=debug):
                score = get.score(album)
                if score and score < lowerlimit:
                    foundLimit = True
                    break
                else:
                    yield album


def aoty_tracks(
    url: str,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> tuple[list[dict[str, str | int]], str]:
    result = page(url, no_list=True)
    for data in search.lines(
        r"^Track List", result, end="Total Length: ", after=1
    ):
        data = data.group().splitlines()
    tracks = list()  # type: list[dict[str, str | int]]
    t = dict()  # type: dict[str, str | int]
    disc = None
    for d in data[2:]:
        if not d:
            continue
        d = str(d)
        if debug:
            print(d)
        if bool(re.search(r"[ ]{3}Total Length: ", d)):
            length = d.replace("Total Length: ", "").replace(" hour, ", ":")
            length = length.replace(" minutes", "").strip()
            return tracks, length
        elif "rating" in t:
            tracks.append(t.copy())
            t.clear()
        if bool(re.search(r"^[ ]{3}Disc \d+", d)):
            disc = d.replace("Disc ", "").strip()
        elif "number" not in t and bool(re.search(r"^[ ]{3}\d+ ", d)):
            t["number"] = ((disc + "-" if disc else "") + d.split(" ", 1)[0])
            t["number"] = str(t["number"]).strip()
            t["title"] = d.split(" ", 1)[1].strip()
        elif "duration" not in t and bool(re.search(r"^[ ]{3}\d+:\d+$", d)):
            t["duration"] = d.strip()
        elif "featuring" not in t and bool(re.search(r"^[ ]{3}feat. ", d)):
            t["featuring"] = d.replace("feat. ", "").strip()
        elif "rating" not in t and bool(re.search(r"^[ ]{3}\d+$", d)):
            t["rating"] = int(d.strip())
        elif bool(re.search(r"^[ ]{4} \d+", d)):
            t["title"] = str(t["title"]) + "\n" + d
        else:
            disc = d.strip()
    print("ERROR: EOF without length.")
    exit(1)
    return tracks, length


def aoty(
    albumType: str,
    pageNumber: int,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator:
    if verbose:
        print(f"- Downloading {albumType}, page {pageNumber}...")
    basePage = "albumoftheyear.org/ratings/user-highest-rated"
    pg = f"{basePage}/{albumType}/all/{pageNumber}/"
    result = page(pg, no_list=True)
    for data in search.lines(r"\d\. ", result, end=r"\d ratings"):
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


def proggenres(
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator:
    pg = "https://www.progarchives.com/"
    data = page(pg, list_only=True)
    for lines in search.lines(r"subgenre\.asp\?style=", data):
        yield lines.group().split("=")[-1]


def proggenre(
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
