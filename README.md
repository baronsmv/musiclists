# MusicLists

## Description

A command-line tool for downloading, filtering, and transforming top album and
track lists from music review websites.

The tool helps you easily aggregate and explore curated album rankings across
different platforms, making it ideal for music enthusiasts and data-driven
listeners.

### Features

- Download lists of the top albums and tracks from multiple platforms such as
  [AlbumOfTheYear.org](https://www.albumoftheyear.org/) and
  [ProgArchives.com](https://www.progarchives.com/).
- Find local albums and tracks in directories and add them to a list.
- Manipulate individually the lists via filtering, sorting, and limiting of
  entries.
- Operate between lists as sets (union, intersection, difference).
- Export to a text file.

### Planned Features

- Copy albums of a list, from a directory to another.
- Convert local albums lists (including transformed ones) to playlists.

### Dependencies

- `bs4`, to navigate and parse HTML tags and values.
- `click` and `click_help_colors`, to implement the CLI.
- `mutagen`, to extract metadata from track files.
- `polars`, to storage and manipulate data.

## Commands

```
Usage: musiclists [OPTIONS] COMMAND [ARGS]...

Commands:
  download    Download lists of albums and tracks from music databases.
  duplicates  Manage duplicated entries between lists.
  export      Export lists to other formats.
  files       Get and manage albums and tracks data from files.
  transform   Transform, merge and compare lists.
```

### Subcommands of download

```
Usage: musiclists download [OPTIONS] COMMAND [ARGS]...

Commands:
  aoty  Download a list of top albums and tracks from AlbumOfTheYear.org.
  prog  Download a list of top albums and tracks from ProgArchives.com.
```

### Subcommands of transform

```
Usage: musiclists transform [albums|tracks] [OPTIONS] COMMAND [ARGS]...

Commands:
  diff       Find the difference between lists.
  filter     Filter a list.
  intersect  Join lists, only returning entries that are in both lists.
  union      Merge downloaded lists into one, returning any entry of each.
```

## Options

### Downloading a list

```
Usage: musiclists download [aoty|prog] [OPTIONS]

Options:
  -t, --types                     Types of albums to download.
  -c, --ceil / -f, --floor        Round up (ceil) or down (floor) the score.
  -s, --min-score INTEGER         Minimum score threshold for including
                                  albums.
  -S, --max-score INTEGER         Maximum score threshold for including
                                  albums.
```

### Finding duplicated entries

```
Usage: musiclists duplicates find [OPTIONS] [SEARCH]...

Options:
  -c, --columns                   Columns to consider for the process.
  -d, --data-1                    Source for the data 1.
  -D, --data-2                    Source for the data 2.
  -H, --highest / -A, --all-matches
                                  Returns only the highest match of each
                                  entry, or every match.
  -s, --min-rate FLOAT            Minimum rate of similarity for including
                                  matches.
  -r, --max-results INTEGER       Limit of results to return.
```

### Exporting or filtering a list

```
Usage: musiclists export [albums|tracks] [OPTIONS]

Options:
  -m, --markdown / --no-markdown  Output as MarkDown.
  -d, --data                      Source for the data.
  -n, --name TEXT                 Use a personalized name instead of an auto-
                                  generated one.
  -s, --min-score INTEGER         Minimum score threshold for including
                                  tracks.
  -S, --max-score INTEGER         Maximum score threshold for including
                                  tracks.
  --min-album-score FLOAT         Minimum score threshold for including
                                  albums.
  --max-album-score FLOAT         Maximum score threshold for including
                                  albums.
  -r, --min-ratings INTEGER       Minimum ratings for including entries.
  -R, --max-ratings INTEGER       Maximum ratings for including entries.
  -c, --columns                   Columns to include.
  -C, --sort-by                   Columns to sort by.
  -a, --limit-album INTEGER       Limit of albums returned per album column.
  -A, --limit-artist INTEGER      Limit of tracks returned per artist column.
  -y, --limit-year INTEGER        Limit of tracks returned per year column.
```

### Getting a set operation result between two lists

```
Usage: musiclists transform [albums|tracks] [diff|intersect|union] [OPTIONS]

Options:
  -d, --data-1                    Source for the data 1.
  -D, --data-2                    Source for the data 2.
  -n, --name TEXT                 Use a personalized name instead of an auto-
                                  generated one.
  -c, --columns                   Columns to consider for the process.
  -k, --key                       Key for the process.
  -d, --dedup / --no-dedup        Deduplicate the output based on its
                                  deduplicates file.
  -K, --dedup-key                 Key for the dedup process.
```

## Donating and Supporting

If you like this project or it's helpful to you in any way, consider
supporting and donating to the websites that made it possible, helping them
keep running:

- [Help Support Album of the Year](https://www.albumoftheyear.org/donate/)
- [Help Support Prog Archives](https://www.paypal.com/donate/?hosted_button_id=DRNRB8RG8NUN2)
