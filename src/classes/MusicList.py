from difflib import SequenceMatcher
from typing import Iterator, Self
from warnings import warn

import polars as pl

from src.classes.Album import Album
from src.classes.DuplicatesList import DuplicatesList
from src.debug import logging
from src.defaults import defaults
from src.defaults.path import TYPE, LOCATION
from src.get.file import path, source


def export_config(markdown: bool) -> pl.Config:
    return pl.Config(
        fmt_str_lengths=30,
        tbl_cell_numeric_alignment="RIGHT",
        tbl_cols=-1,
        tbl_formatting="MARKDOWN" if markdown else "NOTHING",
        tbl_hide_dataframe_shape=True,
        tbl_hide_column_data_types=True,
        tbl_rows=1000000000,
        tbl_width_chars=300,
    )


def choice(
    matches: tuple[Album, ...],
    initial_prompt: str,
    side_by_side: Album | None = None,
    choice_prompt: str = "Choose the desired option (0 to abort)",
    accept_prompt: str = "Accept the match?",
    final_prompt: str | None = None,
    any_to_abort: bool = False,
) -> Album | None:
    while True:
        if len(matches) > 1:
            i = input(
                f"\n{initial_prompt}:\n\n"
                + (f"   {side_by_side}\n" if side_by_side is not None else "")
                + "\n".join(
                    f"{n:4}) {m}" for n, m in enumerate(matches, start=1)
                )
                + f"\n\n{choice_prompt} [0-{len(matches)}]: "
            )
            if i.isdigit():
                i = int(i)
                if 0 < i <= len(matches):
                    match = matches[i - 1]
                    break
                elif i == 0:
                    return None
            elif not i and any_to_abort:
                return None
        else:
            i = input(
                f"\n{initial_prompt}:\n\n"
                + (f"   {side_by_side}\n" if side_by_side is not None else "")
                + f"   {matches[0]}"
                + f"\n\n{accept_prompt} [y/"
                + ("N" if any_to_abort else "n")
                + "]: "
            )
            if i.upper() == "Y":
                match = matches[0]
                break
            elif i.upper() == "N" or (not i and any_to_abort):
                return None
    if final_prompt:
        print(final_prompt)
    return match


class MusicList(pl.DataFrame):
    name = ""
    type = "albums"
    location = "download"
    exists = False

    def __str__(self) -> str:
        return self.name

    def get_attrs(self, other: Self) -> Self:
        self.name = other.name
        self.type = other.type
        self.location = other.location
        self.exists = other.exists
        return self

    def unpack_attrs(self, name: str, type_: TYPE, location: LOCATION) -> Self:
        self.name, self.type, self.location, self.exists = source(
            name, type_, location
        )
        return self

    def to_string(self, markdown: bool) -> str:
        with export_config(markdown):
            ml = str(pl.DataFrame(self))
            if markdown:
                ml = ml.replace("$", "\$")
        return ml

    def albums(self) -> Iterator[Album]:
        for r in self.rows(named=True):
            yield Album(r)

    def tracks(self) -> Self:
        ml = self.explode("tracks")
        ml = pl.concat(
            [
                ml,
                pl.json_normalize(
                    ml["tracks"],
                    infer_schema_length=None,
                ),
            ],
            how="horizontal",
        ).drop("tracks")
        ml = ml.with_columns(
            (
                pl.col("id").cast(pl.Utf8)
                + pl.col("track_number").cast(pl.Utf8).str.zfill(4)
                + pl.col("track_title").cast(pl.Utf8).str.slice(0, 5)
            ).alias("track_id")
        )
        ml = MusicList(ml).get_attrs(self)
        ml.type = "tracks"
        return ml

    def search_album(
        self,
        search_text: str,
        columns: list[str] | tuple[str],
        max_results: int,
        in_list: bool,
    ) -> Album | Self | None:
        similar_albums = sorted(
            (
                (
                    sum(
                        SequenceMatcher(
                            None, search_text, str(albums[col])
                        ).ratio()
                        for col in columns
                    ),
                    albums,
                )
                for albums in self.albums()
            ),
            key=lambda row: row[0],
            reverse=True,
        )[:max_results]
        album = choice(
            tuple(similar_album[1] for similar_album in similar_albums),
            f"Found similar refs. of «{search_text}» in «{self}»",
        )
        if album is None:
            return
        return (
            MusicList([dict(album)], infer_schema_length=None).get_attrs(self)
            if in_list
            else album
        )

    def duplicates(self, key: str = "id") -> Self:
        return self.filter(self.select(key).is_duplicated())

    def has_duplicates(self, key: str = "id") -> bool:
        return not self.duplicates(key).is_empty()

    def load(
        self, name: str, type_: TYPE, location: LOCATION | None = None
    ) -> Self:
        if not location:
            name, *location = name.split(".")
            if not location:
                location = "download"
            elif isinstance(location, (list, tuple)) and len(location) > 0:
                location = location[0]
        logger = logging.logger(self.load)
        src = source(name, type_, location)
        if not src[3]:
            logger.error(f"{name} list doesn't exists and cannot be loaded.")
            exit(1)
        ml = MusicList(self.deserialize(path(*src[:3]))).unpack_attrs(*src[:3])
        return ml

    def warn_duplicates(self) -> None:
        if self.has_duplicates():
            table = (
                self.duplicates().select("id", "artist", "album", "year")
            ).to_string(markdown=True)
            warn(
                "Duplicated ID in the DataFrame:\n"
                + table
                + "\nConsider increasing KEY_LENGTH in defaults (current "
                "one: " + str(defaults.ID_LENGTH) + ")."
            )

    def save(
        self,
        name: str | None = None,
        type_: TYPE | None = None,
        location: LOCATION | None = None,
        suffix: str | None = None,
        warn_duplicates: bool = False,
    ) -> None:
        self.unpack_attrs(
            name if name else self.name,
            type_ if type_ else self.type,
            location if location else self.location,
        )
        if warn_duplicates:
            self.warn_duplicates()
        self.serialize(
            path(
                name=self.name,
                type_=self.type,
                location=self.location,
                suffix=suffix,
            )
        )
        self.exists = True

    def table(
        self,
        save: bool = False,
        name: str | None = None,
        as_md: bool = True,
    ) -> str | None:
        txt = self.to_string(markdown=as_md)
        if save:
            with open(
                path(
                    name=(name if name else self.name)
                    + (
                        f"-{ self.location}"
                        if self.location != "download"
                        else ""
                    ),
                    type_=self.type,
                    location="output",
                    suffix="md" if as_md else "txt",
                ),
                "w",
                encoding="utf-8",
            ) as f:
                f.write(txt)
        else:
            return txt

    def append_to(self, other: Self) -> Self:
        return MusicList(
            other.select(self.columns).extend(self).unique()
        ).get_attrs(self)

    def adapt(self, attrs: dict | list, *others: Self) -> bool:
        col = set(self.columns)
        for o in others:
            col &= set(o.columns)  # type: ignore
        if isinstance(attrs, dict):
            for key in [k for k in attrs if k not in col]:
                del attrs[key]
        elif isinstance(attrs, list):
            attrs[:] = [v for v in attrs if v in col]
        return len(attrs) != 0

    def filter_by_num(
        self, attrs: dict[str, tuple[float | None, float | None]]
    ) -> Self:
        if not self.adapt(attrs):
            return self
        return MusicList(
            self.filter(
                (
                    pl.col(k).is_between(
                        v[0] if v[0] else 0, v[1] if v[1] else 1000000000
                    )
                )
                for k, v in attrs.items()
            )
        ).get_attrs(self)

    def sort_by(self, attrs: dict[str, bool]) -> Self:
        if not self.adapt(attrs):
            return self
        return MusicList(
            self.sort(by=attrs.keys(), descending=list(attrs.values()))
        ).get_attrs(self)

    def limit_per(self, attrs: dict[str, int], sort: bool = True) -> Self:
        if not self.adapt(attrs):
            return self
        ml = (
            self.sort_by({"track_score": True, "user_score": True})
            if sort
            else self
        )
        for k, v in attrs.items():
            if v and v > 0:
                ml = ml.group_by(k, maintain_order=sort).head(v)
        return MusicList(ml).get_attrs(self)

    def select_rename(self, attrs: tuple | dict[str, str]) -> Self:
        if not self.adapt(attrs):
            return self
        if isinstance(attrs, tuple):
            return MusicList(self.select(attrs)).get_attrs(self)
        return MusicList(self.select(attrs.keys()).rename(attrs)).get_attrs(
            self
        )

    def contextualize(
        self,
        num_filter: dict[str, tuple[int | None, int | None]] | None,
        sort_by: dict[str, bool] | None,
        limit_per: dict[str, int] | None,
        select_rename: dict | tuple | None,
    ) -> Self:
        ml = self
        if num_filter is not None:
            ml = ml.filter_by_num(num_filter)
        if limit_per is not None:
            ml = ml.limit_per(limit_per)
        if sort_by is not None:
            ml = ml.sort_by(sort_by)
        if select_rename is not None:
            ml = ml.select_rename(select_rename)
        return ml

    def duplicates_with(self, other: Self) -> DuplicatesList | None:
        name, _, _, exists = source(
            f"{self}-{other}", type_=self.type, location="dedup"
        )
        return DuplicatesList().load(name, type_=self.type) if exists else None

    def duplicated_ids_with(
        self, other: Self, key: str = "id"
    ) -> tuple | None:
        ids = self.duplicates_with(other)
        return (
            ids.get_column(f"{key}-{self}").to_list()
            if ids is not None
            else None
        )

    def yield_duplicates_with(
        self,
        other: Self,
        columns: list[str] | tuple[str],
        max_results: int,
        min_rate: int | float,
        only_highest_match: bool,
        num_diff: float,
    ) -> Iterator[tuple[Album, Album]] | None:
        albums = tuple(MusicList(self.sort(by="id")).albums())
        other_albums = other.albums()
        duplicated_ids = self.duplicated_ids_with(other)
        for album in albums:
            if duplicated_ids is not None and album["id"] in duplicated_ids:
                print(f"«{album}» already has a match.")
                continue
            matches = album.matches_with(
                other_albums, columns, num_diff, min_rate, max_results
            )
            if len(matches) == 0:
                print(f"No matches for «{album}».")
                continue
            if (
                matches[0][0] == 1
                or max(
                    matches[0][2].similarity_with(d, columns, num_diff)
                    for d in albums
                )
                == 1
            ):
                print(f"«{album}» already has a match by ID.")
                continue
            if only_highest_match:
                match_message = (
                    f"Found match ({round(matches[0][0] * 100)}%) between",
                    matches[0][1],
                    matches[0][2],
                )
                c = choice(
                    (matches[0][2],),
                    match_message[0],
                    side_by_side=match_message[1],
                    final_prompt="Match accepted.",
                    any_to_abort=True,
                )
                if c:
                    yield matches[0][1:]
            else:
                match_message = (
                    "Found matches for",
                    matches[0][1],
                )
                c = choice(
                    tuple(m[2] for m in matches),
                    match_message[0],
                    side_by_side=match_message[1],
                    choice_prompt="Choose the desired match (0 if no match if desired)",
                    final_prompt="Match accepted.",
                    any_to_abort=True,
                )
                if c:
                    yield matches[0][1], c

    def find_duplicates_with(
        self,
        other: Self,
        save: bool = True,
        columns: list | tuple = ("album", "artist", "year"),
        min_rate: int | float = 0.6,
        only_highest_match: bool = defaults.ONLY_HIGHEST_MATCH,
        num_diff: float = 0.25,
        max_results: int = 15,
    ) -> DuplicatesList | None:
        matches = tuple(
            self.yield_duplicates_with(
                other=other,
                columns=columns,
                max_results=max_results,
                min_rate=min_rate,
                only_highest_match=only_highest_match,
                num_diff=num_diff,
            )
        )
        if len(matches) == 0:
            return
        data = []
        for m in matches:
            data.append(
                dict(
                    {
                        f"{c}-{d}": m[i][c]
                        for i, d in enumerate((self, other))
                        for c in (
                            "id",
                            "internal_id",
                            "artist",
                            "album",
                            "year",
                        )
                    }
                )
            )
        duplicates = DuplicatesList(data)
        duplicates.name = f"{self}-{other}"
        duplicates.type = self.type
        if save:
            duplicates.save()
        else:
            return duplicates

    def deduplicated_from(
        self,
        other: Self,
        key: str = "internal_id",
    ) -> Self:
        data_2_keys = other.get_column(key)
        col_1 = f"{key}-{self}"
        col_2 = f"{key}-{other}"
        dedup_keys = self.duplicates_with(other)
        if dedup_keys is None or dedup_keys.is_empty():
            return self
        dedup_keys = dedup_keys.select(col_1, col_2).to_dicts()
        return MusicList(
            self.filter(
                pl.col(key)
                .is_in(
                    tuple(
                        k[col_1] for k in dedup_keys if k[col_2] in data_2_keys
                    )
                )
                .not_(),
            )
        )

    def union_with(
        self,
        other: Self,
        columns: tuple,
        save: bool = True,
        name: str | None = None,
        key: str = "id",
        dedup: bool = True,
        dedup_key: str = "internal_id",
    ) -> Self | None:
        columns = list(columns)
        self.adapt(columns, other)
        if key not in columns:
            columns += (key,)
        if dedup_key not in columns:
            columns += (dedup_key,)
        data = self.select(columns)
        other_data = (
            other.deduplicated_from(self, key=dedup_key) if dedup else other
        ).select(columns)
        union = MusicList(data.extend(other_data).unique(key, keep="first"))
        union.name = name if name else f"{self}-{other}"
        union.type = self.type
        union.location = "union"
        if save:
            union.save()
        else:
            return union

    def intersect_with(
        self,
        other: Self,
        columns: tuple,
        save: bool = True,
        name: str | None = None,
        key: str = "id",
    ):
        columns = list(columns)
        self.adapt(columns, other)
        if key not in columns:
            columns += (key,)
        data = self.select(columns)
        other_data = set(other.get_column(key))
        if di := other.duplicated_ids_with(self, key):
            other_data |= set(di)
        intersect = MusicList(data.filter(pl.col(key).is_in(other_data)))
        intersect.name = name if name else f"{self}-{other}"
        intersect.type = self.type
        intersect.location = "intersect"
        if save:
            intersect.save()
        else:
            return intersect

    def diff_with(
        self,
        other: Self,
        columns: tuple,
        save: bool = True,
        name: str | None = None,
        key: str = "id",
        dedup: bool = True,
        dedup_key: str = "internal_id",
    ) -> Self | None:
        columns = list(columns)
        self.adapt(columns, other)
        if key not in columns:
            columns += (key,)
        if dedup_key not in columns:
            columns += (dedup_key,)
        data = (
            self.deduplicated_from(other, key=dedup_key) if dedup else self
        ).select(columns)
        other_data = set(other.get_column(key))
        diff = MusicList(data.filter(pl.col(key).is_in(other_data).not_()))
        diff.name = name if name else f"{self}-{other}"
        diff.type = self.type
        diff.location = "diff"
        if save:
            diff.save()
        else:
            return diff
