#!/usr/bin/env python3

import re
from datetime import timedelta
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

from src.debug import logging
from src.defaults import defaults
from src.html_tags import aoty as aoty_tags


def table(
    url: str,
    tag: str | None = None,
    id: str | None = None,
    number: int = 0,
    user_agent: str = "Mozilla/5.0",
    encoding: str = "utf-8",
    parser: str = "html.parser",
    recursive: bool = True,
    debug: bool = defaults.DEBUG,
):
    logger = logging.logger(table)
    if debug:
        logger.info(
            "Getting table from url: "
            + (url if url else "N/A")
            + ", tag: "
            + (tag if tag else "N/A")
            + " and id: "
            + (id if id else "N/A")
        )
    data = None
    req = Request(url=url, headers={"User-Agent": user_agent})
    if debug:
        logger.info("Request successful.")
    with urlopen(req) as response:
        html = response.read().decode(encoding)
    if debug:
        logger.info("Got response from web server.")
    soup = BeautifulSoup(html, parser)
    if debug:
        logger.info("Parse with BS4 completed.")
    if soup:
        data = (
            soup.find_all(tag, id=id, recursive=recursive)
            if tag and id
            else soup.find_all(tag, recursive=recursive)
            if tag
            else soup.find_all(id=id, recursive=recursive)
            if id
            else None
        )
    return (
        data[number]
        if data and len(data) > abs(number + 1 if number < 0 else number)
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


def tag(
    element,
    data_struct: dict,
    tags: dict,
    include_none: bool = defaults.INCLUDE_NONE,
) -> None:
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
        elif include_none:
            data_struct[k] = None


def aoty_tracks(
    url: str,
    id: str = "tracklist",
    user_agent: str = "Mozilla/5.0",
    encoding: str = "utf-8",
    parser: str = "html.parser",
    tags: dict = aoty_tags.tracklist,
    include_none: bool = defaults.INCLUDE_NONE,
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> tuple[list[dict[str, str | int | list | timedelta]], timedelta]:
    logger = logging.logger(aoty_tracks)
    if debug:
        logger.info(f"Initiating tracklist scrapping of {url}")
    tracklist = table(
        url=url,
        id=id,
        user_agent=user_agent,
        encoding=encoding,
        parser=parser,
        debug=debug,
    )
    tracks = list()  # type: list[dict[str, str | int | list | timedelta]]
    total_length = timedelta()
    disc = str()
    for t in tracklist.find_all("tr"):
        track = dict()  # type: dict[str, str | int | list | timedelta]
        tag(
            element=t,
            data_struct=track,
            tags=tags,
            include_none=include_none,
        )
        if track:
            if "disc" in track:
                disc = str(track["disc"])
            elif disc:
                track["disc"] = disc
            if "length" in track:
                le = str(track["length"]).split(":")
                delta = timedelta(
                    hours=int(le[-3]) if len(le) > 2 else 0,
                    minutes=int(le[-2]) if len(le) > 1 else 0,
                    seconds=int(le[-1]) if len(le) > 0 else 0,
                )
                track["length"] = delta
                total_length += delta
            tracks.append(track.copy())
            track.clear()
        elif debug:
            logger.debug(f"No track data for:\n{t}")
    if tracks:
        if debug:
            logger.info(f"Returning successfully tracklist for {url}")
        return tracks, total_length
    elif tracklist.find("ol", recursive=True).find_all("li"):
        if debug:
            logger.info(
                f"Returning successfully simplified tracklist for {url}"
            )
        return [
            {"title": li.string}
            for li in tracklist.find("ol", recursive=True).find_all("li")
        ], total_length
    else:
        logger.error(f"Didn't find any tracklist for {url}")
        if debug:
            logger.debug(tracklist)
        exit(1)


def prog_genres(
    prog_url: str = "https://www.progarchives.com",
    id_table: str = "navGenre",
    encoding: str = "latin1",
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
) -> dict:
    prog_table = table(url=prog_url, id=id_table, encoding=encoding)
    return {
        g.string: int(g.get("href").split("=")[-1])
        for g in prog_table.find_all("a", recursive=True)
        if g.get("href")
    }


def prog_distribution_score(album_url: str) -> dict[str, int]:
    prog_table = table(url=album_url, tag="blockquote", encoding="latin1")
    for t in prog_table.select("img") + prog_table.select("div"):
        t.extract()
    r = iter(range(5, 0, -1))
    return {
        str(next(r)) + "stars": int(re.sub(r"\D", "", i))
        for i in str(prog_table).splitlines()
        if re.search(r"\d+\%", i)
    }


def prog_tracks(
    album_url: str,
    include_none: bool = defaults.INCLUDE_NONE,
) -> tuple:
    prog_table = table(
        url=album_url, tag="td", number=1, encoding="latin1"
    ).find_all("p")
    tracklist = re.sub(
        r"^<p.*?>", "", str(prog_table[0]).replace("<br/>", "\n")
    )
    r_tracklist = re.compile(
        r"((?P<track_disc>^[a-zA-Z].*?):\n)?"
        + r"(?P<track_number>\d+)\. "
        + r"(?P<track_title>.*?) "
        + r"\((?P<track_length>\d+\:\d+)\)"
        + r"( :(?P<subtracks>(\n-.*)+))?"
        + r"( (?P<track_extras>.*))?\n",
        re.MULTILINE,
    )
    tracks = [t.groupdict() for t in r_tracklist.finditer(tracklist)]
    extras = dict(
        (str(t).replace("</p>", "").split(maxsplit=1))
        for t in re.findall(r"(?:\n)([\$|\#|\*] .*)", tracklist)
    )
    total_length = timedelta()
    disc = str()
    for t in tracks:
        if t["track_length"]:
            le = str(t["track_length"]).split(":")
            delta = timedelta(
                hours=int(le[-3]) if len(le) > 2 else 0,
                minutes=int(le[-2]) if len(le) > 1 else 0,
                seconds=int(le[-1]) if len(le) > 0 else 0,
            )
            t["track_length"] = delta
            total_length += delta
        if disc:
            t["track_disc"] = disc
        elif t["track_disc"]:
            disc = t["track_disc"]
        elif not include_none:
            del t["track_disc"]
        if t["subtracks"]:
            t["subtracks"] = (
                t["subtracks"].replace("\n- ", "", 1).split("\n- ")
            )
        elif not include_none:
            del t["subtracks"]
        if t["track_extras"]:
            t["track_extras"] = t["track_extras"].split()
            t["track_extras"] = [
                extras[e] for e in t["track_extras"] if e in extras
            ]
        if not t["track_extras"] and not include_none:
            del t["track_extras"]
    return tracks, total_length
