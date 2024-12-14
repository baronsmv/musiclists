import re
from collections import UserDict
from difflib import SequenceMatcher
from statistics import median
from typing import Self, Iterator
from unicodedata import normalize

from src.defaults.defaults import ALBUM_REPR_SEP, ID_LENGTH, ID_SEP


class Album(UserDict):
    def __str__(self):
        return (
            self.get("artist", "")
            + ALBUM_REPR_SEP
            + self.get("album", "")
            + " ("
            + str(self.get("year"))
            + ")"
        )

    def compute_id(self) -> None:
        result = ""
        sep_length = len(ID_SEP)
        for attr in ("artist", "year", "album"):
            field = self.get(attr, None)
            if field is None:
                continue
            field = str(field)
            for pattern in (r"[Tt]he ", r" EP", r".*: "):
                field = re.sub(pattern, "", field)
            field = str(normalize("NFKD", field).encode("ascii", "ignore"))[2:]
            field = re.sub(r"[^0-9a-zA-Z]+", "", field)
            field = field[:ID_LENGTH].lower()
            result += ID_SEP + field
        self["id"] = result[sep_length:]

    def similarity_with(
        self,
        other: Self,
        columns: list[str] | tuple[str],
        num_diff: float = 0.25,
    ) -> float:
        return median(
            (
                SequenceMatcher(None, self[col], str(other[col])).ratio()
                if isinstance(self[col], str)
                else 1 - (abs(self[col] - other[col]) * num_diff)
            )
            for col in columns
        )

    def matches_with(
        self,
        other_albums: Iterator[Self],
        columns: tuple,
        num_diff: float,
        min_rate: float,
        max_results: int,
    ) -> list[tuple[float, Self, Self]]:
        return sorted(
            (
                (sim, self, other_album)
                for other_album in other_albums
                if (
                    sim := self.similarity_with(other_album, columns, num_diff)
                )
                >= min_rate
            ),
            key=lambda row: row[0],
            reverse=True,
        )[:max_results]