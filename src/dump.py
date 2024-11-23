#!/usr/bin/env python3

from bs4 import BeautifulSoup
from collections.abc import Iterator
from pathlib import Path
import re
from urllib.request import Request, urlopen
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


def aoty_tracks(
    url: str,
    user_agent: str = "Mozilla/5.0",
    encoding: str = "utf-8",
    list_id: str = "tracklist",
    base_page: str = "https://www.albumoftheyear.org",
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> list[dict[str, str | int | list]]:
    req = Request(url=url, headers={"User-Agent": user_agent})
    with urlopen(req) as response:
        html = response.read().decode(encoding)
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find(id=list_id, recursive=True)
    tracks = list()  # type: list[dict[str, str | int | list]]
    for t in table.find_all("tr"):  # type: ignore
        track = dict()
        for k, v in {
            "track": "trackNumber",
            "title": "trackTitle",
            "length": "length",
            "featuring": "featuredArtists",
            "score": "trackRating",
        }.items():
            data = t.find(("td", "div"), class_=v)
            if data:
                if k == "title":
                    data = data.find("a")
                    track[k] = data.string
                    track["url"] = base_page + data.get("href")
                elif k == "score":
                    data = data.find("span")
                    track[k] = int(data.text)
                    track["ratings"] = data.get("title").split()[0]
                elif k == "featuring":
                    track[k] = [
                        {"artist": d.text, "url": d.get("href")}
                        for d in data.find_all("a")
                    ]
                else:
                    track[k] = data.string
        if track:
            tracks.append(track)
    return tracks


def aoty(
    albumType: str,
    pageNumber: int,
    include_url: bool = defaults.INCLUDE_URL,
    include_tracks: bool = defaults.INCLUDE_TRACKS,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> Iterator:
    if verbose:
        print(f"- Downloading {albumType}, page {pageNumber}...")
    basePage = "albumoftheyear.org/ratings/user-highest-rated"
    pg = f"{basePage}/{albumType}/all/{pageNumber}/"
    result = page(pg, no_list=True)
    if include_url or include_tracks:
        result_w_list = page(pg)
    for data in search.lines(r"\d\. ", result, end=r"\d ratings"):
        base = 0
        lines = data.group().splitlines()
        line = lines[base + 0].strip().split(". ", 1)
        if include_url or include_tracks:
            url = get.url(result_w_list, r"[^\d]" + line[0] + r"\. ")
        if include_tracks:
            tracks = aoty_tracks(url, verbose=verbose, debug=debug)
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
        ratings = int(lines[base + 7].strip().split(" ")[0].replace(",", ""))
        album = {
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
        if include_url:
            album["url"] = url
        if include_tracks:
            album["tracks"] = tracks
        yield {get.id((artist, year, title)): album}


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
