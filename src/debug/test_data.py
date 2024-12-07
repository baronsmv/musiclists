#!/usr/bin/env python3

import unittest

from src import dump


class AOTYTestCase(unittest.TestCase):
    quiet = True
    album_type = "lp"
    page_number = 1
    page_msg = (
        f"AOTY page {page_number} of type {album_type} cannot be retrieved."
    )
    expected_albums = 25
    member = "album"

    print("Retrieving AOTY albums...")
    albums = tuple(
        dump.aoty(
            album_type=album_type,
            page_number=page_number,
            quiet=quiet,
        )
    )

    def test_aoty_page(self):
        self.assertTrue(self.albums, msg=self.page_msg)

    def test_aoty_page_length(self):
        self.assertEqual(len(self.albums), self.expected_albums)

    def test_aoty_member(self):
        self.assertIn(self.member, self.albums)


if __name__ == "__main__":
    unittest.main()
