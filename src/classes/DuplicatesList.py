from typing import Self

import polars as pl

from src.debug import logging
from src.defaults.choice import ALBUMS_DEDUP
from src.defaults.path import TYPE
from src.get.file import path, source


class DuplicatesList(pl.DataFrame):
    name = ""
    type = TYPE
    exists = False

    def get_attrs(self, other: Self) -> Self:
        self.name = other.name
        self.exists = other.exists
        return self

    def unpack_attrs(self, name: str, type_: TYPE) -> Self:
        self.name, self.type, _, self.exists = source(
            name=name, type_=type_, location="dedup", order=True
        )
        return self

    def append(self):
        return DuplicatesList(
            self.load(
                self.name,
                self.type,
            )
            .extend(self)
            .unique()
        ).get_attrs(self)

    def load(self, name: str, type_: TYPE) -> Self:
        logger = logging.logger(self.load)
        dl = self.unpack_attrs(name, type_=type_)
        dl = DuplicatesList(
            self.deserialize(path(name, type_=type_, location="dedup"))
        ).get_attrs(dl)
        if not dl.exists:
            logger.error(f"Couldn't find {name} in {ALBUMS_DEDUP.keys()}.")
            exit(1)
        return dl

    def save(self, name: str | None = None) -> None:
        self.unpack_attrs(
            name if name else f"{self.name}.{self.type}", type_=self.type
        )
        (self.append() if self.exists else self).serialize(
            path(name=self.name, type_=self.type, location="dedup")
        )
        self.exists = True
