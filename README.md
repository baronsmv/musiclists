# MusicLists

## Description

A command-line tool for downloading, filtering, and transforming top album and
track lists from websites like AOTY.org and ProgArchives.com.

The tool helps you easily aggregate and explore curated album rankings across
different platforms, making it ideal for music enthusiasts and data-driven
listeners.

### Features

- Download lists of the top albums and tracks from multiple platforms such as
  AlbumOfTheYear.org and ProgArchives.com.
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
musiclists [OPTIONS] COMMAND [ARGS]...

Commands:
  download    Download lists of albums and tracks from music databases.
  duplicates  Manage duplicated entries between lists.
  export      Export lists to other formats.
  files       Get and manage albums and tracks data from files.
  transform   Transform, merge and compare lists.
```

### Subcommands of download

```
musiclists download [OPTIONS] COMMAND [ARGS]...

Commands:
  aoty  Download a list of top albums and tracks from AlbumOfTheYear.org.
  prog  Download a list of top albums and tracks from ProgArchives.com.
```

### Subcommands of transform

```
Usage: musiclists transform tracks [OPTIONS] COMMAND [ARGS]...

Commands:
  diff       Find the difference between lists.
  filter     Filter a list of tracks.
  intersect  Join lists, only returning tracks that are in both lists.
  union      Merge downloaded lists into one, returning any album of each.
```

## Options

### Downloading a list

```
Usage: musiclists download prog [OPTIONS]

Options:
  -t, --types [all|Studio|DVD|Boxset,Compilation|Live|Singles,EPs,FanClub,Promo]
                                  Types of ProgArchives albums to download.
  -c, --ceil / -f, --floor        Round up (ceil) or down (floor) the score.
  -s, --min-score INTEGER         Minimum score threshold for including
                                  ProgArchives albums.
  -S, --max-score INTEGER         Maximum score threshold for including
                                  ProgArchives albums.
```

### Finding duplicated entries

```
musiclists duplicates find [OPTIONS] [SEARCH]...

Options:
  -c, --columns [all|id|internal_id|artist|album|year|type|position|user_score|user_ratings|album_path|album_url|cover_url]
                                  Columns to consider for the process.
  -d, --data-1 [aoty|prog]        Source for the data 1.
  -D, --data-2 [aoty|prog]        Source for the data 2.
  -H, --highest / -A, --all-matches
                                  Returns only the highest match of each
                                  entry, or every match.
  -s, --min-rate FLOAT            Minimum rate of similarity for including
                                  matches.
  -r, --max-results INTEGER       Limit of results to return.
```

### Exporting or filtering a list

```
Usage: musiclists export tracks [OPTIONS]

Options:
  -m, --markdown / --no-markdown  Output as MarkDown.
  -d, --data [aoty|prog]          Source for the data.
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
  -r, --min-ratings INTEGER       Minimum ratings for including tracks.
  -R, --max-ratings INTEGER       Maximum ratings for including tracks.
  -c, --columns [all|track_score|track_ratings|track_number|track_title|track_length|track_disc|track_path|featuring|track_url|id|internal_id|artist|album|year|type|position|user_score|user_ratings|album_path|album_url|cover_url]
                                  Columns to include.
  --sort-by [track_score|track_ratings|track_number|track_title|track_length|track_disc|featuring|id|internal_id|artist|album|year|type|position|user_score|user_ratings]
                                  Columns to sort by.
  -a, --limit-album INTEGER       Limit of albums returned per album column.
  -A, --limit-artist INTEGER      Limit of tracks returned per artist column.
  -y, --limit-year INTEGER        Limit of tracks returned per year column.
```

### Getting a set operation result between two lists

```
Usage: musiclists transform tracks diff [OPTIONS]

Options:
  -d, --data-1 [aoty|prog]        Source for the data 1.
  -D, --data-2 [aoty|prog]        Source for the data 2.
  -n, --name TEXT                 Use a personalized name instead of an auto-
                                  generated one.
  -c, --columns [all|track_score|track_ratings|track_number|track_title|track_length|track_disc|track_path|featuring|track_url|id|internal_id|artist|album|year|type|position|user_score|user_ratings|album_path|album_url|cover_url]
                                  Columns to consider for the process.
  -k, --key [id|internal_id]      Key for the diff process.
  -d, --dedup / --no-dedup        Deduplicate the output based on its
                                  deduplicates file.
  -K, --dedup-key [id|internal_id]
                                  Key for the dedup process.
```
