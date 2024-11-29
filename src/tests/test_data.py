#!/usr/bin/env python3

import unittest
from datetime import timedelta

from src import get
from src.html_tags import prog as prog_tags


album = dict()  # type: dict[str, str | int | float | list | dict | timedelta]
album_url = "https://www.progarchives.com/album.asp?id=11072"
album_data = get.table(url=album_url, tag="td", encoding="latin1")
get.tag(element=album_data, data_struct=album, tags=prog_tags.album)
album["score_distribution"] = get.prog_distribution_score(album_url)
album["tracks"], album["total_length"] = get.prog_tracks(album_url)


class TestProgBeatles(unittest.TestCase):

    def test_data(self):
        self.assertTrue(album)

    def test_track(self):
        self.assertEqual(album["tracks"][1]["title"], "Dear Prudence")


main = unittest.main

if __name__ == '__main__':
    main()
