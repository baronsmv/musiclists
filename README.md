# MusicLists

## Description

A command-line tool for downloading, filtering, and transforming top album and
track lists from websites like AOTY.org and ProgArchives.com.

The tool helps you easily aggregate and explore curated album rankings across
different platforms, making it ideal for music enthusiasts and data-driven
listeners.

## Features

- Download lists of the top albums and tracks from multiple platforms such as
  AlbumOfTheYear.org and ProgArchives.com.
- Find local albums and tracks in directories and add them to a list.
- Manipulate individually the lists via filtering, sorting, and limiting of
  entries.
- Operate between lists as sets (union, intersection, difference).
- Export to a text file.

## Planned Features

- Copy albums of a list, from a directory to another.
- Convert local albums lists (including transformed ones) to playlists.

## Dependencies

- `bs4`, to navigate and parse HTML tags and values.
- `click` and `click_help_colors`, to implement the CLI.
- `mutagen`, to extract metadata from track files.
- `polars`, to storage and manipulate data.
