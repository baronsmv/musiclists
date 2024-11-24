#!/usr/bin/env python3

from bs4 import BeautifulSoup
from pathlib import Path
import re
from urllib.request import Request, urlopen

from src.defaults import defaults
from src.html_tags import aoty as aoty_tags
from src import search


def path(
    data: dict,
    sep: str = "/",
    includeyear: bool = True,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> str:
    return (
        data.get("artist", "")
        + sep
        + data.get("title", "")
        + (
            "("
            + str(data.get("year", ""))
            + ")"
            if includeyear
            and data.get("year")
            else ""
        )
    )


def level(
    child: Path,
    parent: Path,
    lvl: int = 0,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> int:
    if child.parent.absolute() == parent.absolute():
        return lvl
    else:
        return level(child.parent, parent, lvl + 1)


def table(
    url: str,
    tag: str | None = None,
    id: str | None = None,
    number: int = 0,
    user_agent: str = "Mozilla/5.0",
    encoding: str = "utf-8",
    parser: str = "html.parser",
    recursive: bool = True,
):
    req = Request(url=url, headers={"User-Agent": user_agent})
    with urlopen(req) as response:
        html = response.read().decode(encoding)
    soup = BeautifulSoup(html, parser)
    if soup:
        table = (
            soup.find_all(tag, id=id, recursive=recursive)
            if tag and id
            else soup.find_all(tag, recursive=recursive)
            if tag
            else soup.find_all(id=id, recursive=recursive)
            if id
            else None
        )
    return (
        table[number]
        if table and len(table) > abs(number + 1 if number < 0 else number)
        else None
    )


def find_tag(element, values):
    if "tag" in values:
        if "class" in values:
            d = element.find_all(
                values["tag"], class_=values["class"], recursive=True
            )
        else:
            d = element.find_all(values["tag"])
        i = values["number"] if "number" in values else 0
        if len(d) > abs(i + 1 if i < 0 else i):
            return d[i]
        else:
            return None
    else:
        return element


def tag(element, data_struct: dict, tags: dict) -> None:
    for k, v in tags.items():
        d = find_tag(element=element, values=v)
        if d and "subtag" in v:
            d = find_tag(element=d, values=v["subtag"])
        if d and "key" in v:
            d = d.get(v["key"])
        if d and "contains" in v and isinstance(v["contains"], dict):
            data_struct[k] = None
            tag(element=d, data_struct=data_struct, tags=dict(v["contains"]))
        if d and "expand" in v:
            if "expand_url" in v:
                d = list(
                    {v["expand_url"]: e.get_text(), "url": e.get("href")}
                    for e in d.find_all(v["expand"])
                    if e.get("href") != "#"
                )
            else:
                d = list(e.get_text() for e in d.find_all(v["expand"]))
        if d and ("type" in v or "replace" in v or "match" in v):
            if not isinstance(d, str) and (
                any(v["type"] == t for t in ("str", "int", "float"))
            ):
                d = d.get_text().strip()
            if "match" in v:
                d = re.search(v["match"], d)
                d = d.group() if d else None
            if "replace" in v and isinstance(v["replace"], dict):
                for kr, vr in v["replace"].items():
                    d = d.replace(kr, vr)
            if any(v["type"] == t for t in ("int", "float")):
                d = (
                    int(d)
                    if v["type"] == "int" and d.isdigit()
                    else float(d)
                    if v["type"] == "float" and d.replace(".", "", 1).isdigit()
                    else None
                )
        if d:
            data_struct[k] = d


def aoty_tracks(
    url: str,
    id: str = "tracklist",
    user_agent: str = "Mozilla/5.0",
    encoding: str = "utf-8",
    parser: str = "html.parser",
    tags: dict = aoty_tags.tracklist,
    base_page: str = "https://www.albumoftheyear.org",
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> list[dict[str, str | int | list]]:
    if debug:
        print(url)
    tracklist = table(
        url=url,
        id=id,
        user_agent=user_agent,
        encoding=encoding,
        parser=parser
    )
    tracks = list()  # type: list[dict[str, str | int | list]]
    disc = str()
    for t in tracklist.find_all("tr"):
        track = dict()  # type: dict[str, str | int | list]
        tag(element=t, data_struct=track, tags=tags)
        if track:
            if "disc" in track:
                disc = str(track["disc"])
            elif disc:
                track["disc"] = disc
            tracks.append(track.copy())
            track.clear()
    if tracks:
        return tracks
    elif tracklist.find("ol", recursive=True).find("li"):
        return [
            {"title": li.string} for li in
            tracklist.find("ol", recursive=True).find_all("li")
        ]
    else:
        print(f"ERROR: Didn't find any tracks for {url}")
        exit(1)


def prog_genres(
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    prog_page = "https://www.progarchives.com"
    prog_table = table(url=prog_page, id="navGenre", encoding="latin1")
    return {
        g.string: int(g.get("href").split("=")[-1])
        for g in prog_table.find_all("a", recursive=True)
        if g.get("href")
    }
