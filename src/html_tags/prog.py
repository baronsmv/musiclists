#!/usr/bin/env python3

albumlist = {
    "position": {
        "tag": "td",
        "subtag": {
            "tag": "strong",
        },
        "type": "int",
    },
    "title": {
        "tag": "a",
        "number": 0,
        "type": "str",
        "contains": {
            "album_url": {
                "key": "href",
                "type": "str",
            },
        },
    },
    "cover_url": {
        "tag": "img",
        "type": "str",
        "key": "src",
    },
    "artist": {
        "tag": "a",
        "number": 1,
        "type": "str",
        "contains": {
            "artist_url": {
                "key": "href",
                "type": "str",
            },
        },
    },
    "year": {
        "tag": "br",
        "number": 1,
        "type": "str",
        "match": r"\d{4}"
    },
    "qwr": {
        "tag": "div",
        "type": "float",
        "number": 1,
        "replace": {"QWR = ": ""},
    },
    "average_rating": {
        "tag": "span",
        "type": "float",
    },
    "ratings": {
        "tag": "span",
        "number": 1,
        "type": "int",
    },
}
album = {
    "reviews": {
        "tag": "span",
        "number": 5,
        "type": "int",
    },
    "score_distribution": {
        "tag": "blockquote",
    }
}
tracklist = {
    "disc": {
        "tag": "div",
        "class": "discNumber",
        "type": "str",
    },
    "track": {
        "tag": "td",
        "class": "trackNumber",
        "type": "int",
    },
    "title": {
        "tag": "td",
        "class": "trackTitle",
        "type": "str",
        "subtag": {
            "tag": "a",
        },
        "contains": {
            "url": {
                "key": "href",
                "type": "str",
            },
        },
    },
    "subtracks": {
        "tag": "div",
        "class": "trackNotes",
        "subtag": {
            "tag": "ul",
        },
        "type": "list_str",
        "expand": "li",
    },
    "length": {
        "tag": "div",
        "class": "length",
        "type": "str",
    },
    "featuring": {
        "tag": "div",
        "class": "featuredArtists",
        "type": "list",
        "expand": "a",
        "expand_url": "artist",
    },
    "score": {
        "tag": "td",
        "class": "trackRating",
        "subtag": {
            "tag": "span",
        },
        "type": "int",
        "contains": {
            "ratings": {
                "key": "title",
                "replace": {" Ratings": ""},
                "type": "int",
            }
        }
    },
}
