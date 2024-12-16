from pathlib import Path
from pprint import pformat

from mutagen import File

from src.attributes.local_dirs import album as album_attr, track as track_attr
from src.classes.Album import Album
from src.classes.MusicList import MusicList
from src.debug import logging
from src.defaults import defaults
from src.dump import dirs


def __extract__(tag: list, key: str, sep: str = "; ") -> str | int:
    tag = sep.join(tag)
    if key in ("year", "total_tracks", "total_discs", "track_number", "disc"):
        tag = int(tag.split("/")[0])
    return tag


def from_dir(
    source: Path,
    suffixes: tuple = ("opus", "mp3", "m4a", "flac"),
    album_data: dict = album_attr,
    track_data: dict = track_attr,
    id_from: str = "musicbrainz_albumid",
    quiet: bool = defaults.QUIET,
    verbose: bool = defaults.VERBOSE,
    debug: bool = defaults.DEBUG,
):
    logger = logging.logger(from_dir)
    albums = []
    album = Album()
    if not quiet:
        print(f"Registering music from '{source}'")
    for d in dirs(source):
        track_files = tuple(
            File(f, easy=True)
            for s in suffixes
            for f in sorted(d.glob(f"*.{s}"))
        )
        if len(track_files) == 0:
            continue
        for k, v in album_data.items():
            tag = track_files[0].get(v)
            if not tag:
                continue
            album[k] = __extract__(tag, k)
        album["album_path"] = d.as_posix()
        if not "year" in album:  # M4a Tags don't have year tag
            if "original_date" in album:
                album["year"] = int(album["original_date"][:4])
            elif "release_date" in album:
                album["year"] = int(album["release_date"][:4])
            else:
                logger.warning(f"No year tag found in album `{album}`.")
        album.compute_id()
        if id_from in track_files[0]:
            album["internal_id"] = track_files[0][id_from]
        else:
            logger.warning(
                f"Couldn't retrieve internal ID with tag `{id_from}` from album "
                f"`{album}`."
            )
            if debug:
                logger.debug(pformat(track_files[0]))
        album["tracks"] = []
        for t in track_files:
            album["tracks"].append(
                {
                    k: __extract__(t[v], k)
                    for k, v in track_data.items()
                    if v in t
                }
                | {"track_path": t.filename}
            )
        albums.append(dict(album.copy()))
        album.clear()
    if not albums:
        logger.error(f"No albums found on `{source}`.")
        exit(1)
    ml = MusicList(albums)
    ml.save(name="dirs")
    ml.tracks().save()


def playlist(data: str):
    pass
