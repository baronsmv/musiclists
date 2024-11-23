#!/usr/bin/env python3

from bs4 import BeautifulSoup
from pathlib import Path
import re
from unicodedata import normalize
from urllib.request import Request, urlopen

from src.defaults import defaults, html_tags
from src import search


def get(
    data: dict,
    key: str,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    if not data.get(key):
        if key in tuple(data.values())[0]:
            return tuple(data.values())[0][key]
        else:
            return str()
    else:
        return data.get(key)


def artist(
    data: dict,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> str:
    return get(data, "artist")


def title(
    data: dict,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> str:
    return get(data, "title")


def year(
    data: dict,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> int:
    return get(data, "year")


def score(
    data: dict,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> int | float:
    return get(data, "score")


def id(
    data: list | tuple | dict[str, str | int | list] | str,
    length: int = 14,
    sep: str = "",
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> str:
    if isinstance(data, str):
        res = re.search(
            r"(?P<artist>^.*)\/(?P<title>.*) \((?P<year>.*)\)", data
        )
        return id(tuple(res.group(p) for p in ("artist", "year", "title")))
    elif isinstance(data, dict):
        return id((artist(data), year(data), title(data)))
    dataStr = str()
    sepL = len(sep)
    for d in data:
        if not d:
            continue
        d = str(d)
        for pattern in (r"[Tt]he ", r" EP", r".*: "):
            d = re.sub(pattern, "", d)
        d = str(normalize("NFKD", d).encode("ascii", "ignore"))[2:]
        d = re.sub(r"[^0-9a-zA-Z]+", "", d)
        d = d[:length].lower()
        dataStr += sep + d
    return dataStr[sepL:]


def path(
    data: dict[str, str | list | int | float],
    sep: str = "/",
    includeyear: bool = True,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> str:
    return (
        artist(data)
        + sep
        + title(data)
        + (f" ({year(data)})" if includeyear else "")
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


def url(
    webpage: str,
    pattern_before: str = str(),
    pattern_after: str = str(),
) -> str:
    count = 0
    for m in search.lines(
        pattern_before + r"\[(?P<url_id>\d{1,})\]" + pattern_after, webpage
    ):
        url_id = m.group("url_id")
        count += 1
    if count != 1:
        print(f"ERROR en URL_ID({count}): {pattern_before}, {pattern_after}")
        exit(1)
    count = 0
    for m in search.lines(r"[^\d]" + url_id + r"\. (?P<url>http.*)", webpage):
        url = m.group("url")
        count += 1
    if count != 1:
        print(f"ERROR en URL({count}): {pattern_before}, {pattern_after}")
        exit(1)
    return url


def table(
    url: str,
    id: str,
    user_agent: str = "Mozilla/5.0",
    encoding: str = "utf-8",
    parser: str = "html.parser",
):
    req = Request(url=url, headers={"User-Agent": user_agent})
    with urlopen(req) as response:
        html = response.read().decode(encoding)
    soup = BeautifulSoup(html, parser)
    return soup.find(id=id, recursive=True)


def tag(element, track: dict, tags: dict) -> None:
    for k, v in tags.items():
        if "tag" in v and "class" in v:
            d = element.find(v["tag"], class_=v["class"])
        elif "key" in v:
            d = element.get(v["key"])
        if d and "subtag" in v:
            d = d.find(v["subtag"])
        if d and "contains" in v and isinstance(v["contains"], dict):
            tag(element=d, track=track, tags=dict(v["contains"]))
        if d and "expand" in v:
            if "type" in v and v["type"] == "list":
                d = list(d.find_all(v["expand"]))
            else:
                d = list(e.string for e in d.find_all(v["expand"]))
        if d and "type" in v or "replace" in v:
            if not isinstance(d, str) and (
                v["type"] == "str"
                or v["type"] == "int"
            ):
                d = d.string
            if "replace" in v and isinstance(v["replace"], dict):
                for kr, vr in v["replace"].items():
                    d = d.replace(kr, vr)
            if v["type"] == "int":
                d = int(d)
        if d:
            track[k] = d


def aoty_tracks(
    url: str,
    id: str = "tracklist",
    user_agent: str = "Mozilla/5.0",
    encoding: str = "utf-8",
    parser: str = "html.parser",
    tags: dict = html_tags.AOTY,
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
    if (
        tracklist.find("ol", recursive=True)
        and not tracklist.find("trackTitle", recursive=True)
    ):
        return [
            {"title": li.string} for li in
            tracklist.find("ol", recursive=True).find_all("li")
        ]
    tracks = list()  # type: list[dict[str, str | int | list]]
    disc = str()
    for t in tracklist.find_all("tr"):
        track = dict()  # type: dict[str, str | int | list]
        tag(element=t, track=track, tags=tags)
        if track:
            if (
                "featuring" in track
                and isinstance(track["featuring"], list)
            ):
                track["featuring"] = [
                    {"artist": tags.text, "url": tags.get("href")}
                    for tags in track["featuring"]
                ]
            if "disc" in track:
                disc = str(track["disc"])
            elif disc:
                track["disc"] = disc
            tracks.append(track.copy())
            track.clear()
    return tracks
