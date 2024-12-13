from typing import Self

import polars as pl

from src.debug import logging
from src.defaults.choice import DEDUP_CHOICE
from src.get.file import get_path, source


class DuplicatesList(pl.DataFrame):
    name = ""
    exists = False

    def get_attrs(self, other: Self) -> Self:
        self.name = other.name
        self.exists = other.exists
        return self

    def append(self):
        return DuplicatesList(
            self.load(self.name).extend(self).unique()
        ).get_attrs(self)

    def load(self, name: str) -> Self:
        logger = logging.logger(self.load)
        dl = self
        _, dl.name, dl.exists = source(f"dedup.{name}")
        dl = DuplicatesList(
            self.deserialize(DEDUP_CHOICE[f"dedup.{dl.name}"])
        ).get_attrs(dl)
        if not dl.exists:
            logger.error(f"Couldn't find {name} in {DEDUP_CHOICE.keys()}.")
            exit(1)
        return dl

    def save(self, name: str) -> None:
        _, self.name, self.exists = source(f"dedup.{name}")
        (self.append() if self.exists else self).serialize(
            get_path(self.name, location="dedup")
        )
        self.exists = True
