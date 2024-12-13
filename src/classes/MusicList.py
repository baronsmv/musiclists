from difflib import SequenceMatcher
from typing import Iterator, Self
from warnings import warn

import polars as pl

from src.classes.Album import Album
from src.classes.DuplicatesList import DuplicatesList
from src.defaults import defaults
from src.defaults.choice import ALL_CHOICE
from src.get.file import get_path, source


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
    location = ""
    exists = False

    def __str__(self) -> str:
        return self.name

    def get_attrs(self, other: Self) -> Self:
        self.name = other.name
        self.location = other.location
        self.exists = other.exists
        return self

    def as_df(self, as_md: bool) -> str:
        with export_config(as_md):
            st = str(pl.DataFrame(self))
        return st

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
        )
        return MusicList(ml).get_attrs(self)

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

    def load(self, name: str) -> Self:
        ml = MusicList(self.deserialize(ALL_CHOICE[name]))
        ml.location, ml.name, ml.exists = source(name)
        if not ml.exists:
            raise KeyError(f"Couldn't find {name} in {ALL_CHOICE.keys()}.")
        return ml

    def warn_duplicates(self) -> None:
        if self.has_duplicates():
            table = (
                self.duplicates().select("id", "artist", "album", "year")
            ).as_df(as_md=True)
            warn(
                "Duplicated ID in the DataFrame:\n"
                + table
                + "\nConsider increasing KEY_LENGTH in defaults (current "
                "one: " + str(defaults.ID_LENGTH) + ")."
            )

    def save(
        self,
        name: str,
        suffix: str | None = None,
        warn_duplicates: bool = False,
    ) -> None:
        self.location, self.name, self.exists = source(name)
        if warn_duplicates:
            self.warn_duplicates()
        self.serialize(get_path(self.name, self.location, suffix=suffix))
        self.exists = True

    def table(
        self,
        save: bool = False,
        name: str | None = None,
        name_prefix: str = "",
        name_postfix: str = "",
        as_md: bool = True,
    ) -> str | None:
        txt = self.as_df(as_md=as_md)
        if save:
            with open(
                get_path(
                    name_prefix
                    + (
                        f"{self.location}-"
                        if self.location != "download"
                        else ""
                    )
                    + (name if name else self.name)
                    + name_postfix,
                    suffix="md" if as_md else "txt",
                    location="output",
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

    def filter_by_num(
        self, attrs: dict[str, tuple[float | None, float | None]]
    ) -> Self:
        col = self.columns
        for k in tuple(attrs.keys()):
            if k not in col:
                del attrs[k]
        if len(attrs) == 0:
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
        col = self.columns
        for k in tuple(attrs.keys()):
            if k not in col:
                del attrs[k]
        if len(attrs) == 0:
            return self
        return MusicList(
            self.sort(by=attrs.keys(), descending=list(attrs.values()))
        ).get_attrs(self)

    def select_rename(self, attrs: dict) -> Self:
        col = self.columns
        for k in tuple(attrs.keys()):
            if k not in col:
                del attrs[k]
        if len(attrs) == 0:
            return self
        return MusicList(self.select(attrs.keys()).rename(attrs)).get_attrs(
            self
        )

    def contextualize(
        self,
        num_filter: dict[str, tuple[int | None, int | None]] | None,
        sort_by: dict[str, bool] | None,
        select_rename: dict | tuple | list | None,
    ) -> Self:
        ml = self
        if num_filter is not None:
            ml = ml.filter_by_num(num_filter)
        if sort_by is not None:
            ml = ml.sort_by(sort_by)
        if select_rename is not None:
            ml = ml.select_rename(select_rename)
        return ml.get_attrs(self)

    def duplicates_with(self, other: Self) -> DuplicatesList | None:
        location, name, exists = source(f"dedup.{self}-{other}")
        return DuplicatesList().load(name) if exists else None

    def duplicated_ids_with(self, other: Self) -> tuple | None:
        ids = self.duplicates_with(other)
        return (
            ids.get_column(f"id-{self}").to_list() if ids is not None else None
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
        if save:
            duplicates.save(duplicates.name)
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

    def merge_with(
        self,
        other: Self,
        columns: tuple,
        save: bool = True,
        key: str = "id",
        dedup: bool = True,
        dedup_key: str = "internal_id",
    ) -> Self | None:
        columns += (key, dedup_key)
        data = self.select(columns)
        other_data = (
            other.deduplicated_from(self, key=dedup_key) if dedup else other
        ).select(columns)
        merged = MusicList(data.extend(other_data).unique(key, keep="first"))
        merged.name = f"{self}-{other}"
        merged.location = "merge"
        if save:
            merged.save(f"{merged.location}.{merged.name}")
        else:
            return merged

    def diff_with(
        self,
        other: Self,
        columns: tuple,
        save: bool = True,
        key: str = "id",
        dedup: bool = True,
        dedup_key: str = "internal_id",
    ) -> Self | None:
        columns += (key, dedup_key)
        data = (
            self.deduplicated_from(other, key=dedup_key) if dedup else self
        ).select(columns)
        other_data = set(other.get_column(key))
        diff = MusicList(data.filter(pl.col(key).is_in(other_data).not_()))
        diff.name = f"{self}-{other}"
        diff.location = "diff"
        if save:
            diff.save(f"{diff.location}.{diff.name}")
        else:
            return diff
