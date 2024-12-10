# MusicLists

## Description

A command-line tool for downloading, merging, and analyzing top album lists
from websites like AOTY.org and ProgArchives.com.

The tool helps you easily aggregate and explore curated album rankings across different platforms, making it ideal for music enthusiasts and data-driven listeners.

## Features

- Download lists of the top albums from multiple platforms such as AOTY.org and ProgArchives.com.
- Provide utilities for merging, subtracting, filtering, sorting, and processing the album data, as well as their tracks.
- Export to multiple formats, for further analysis.

## Planned Features

- Find albums in directories and add them to a list.
- Provide a uility to copy albums of a list, from a directory to another.

## Dependencies

- `bs4`, for navigating HTML tags.
- `click` and `click_help_colors`, used in the CLI.
- `polars`, to storage the data in DataFrames.
- `pathlib`, to deal easily with files and directories.
- `pyexiftool`, to extract data from files.
