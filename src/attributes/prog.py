#!/usr/bin/env python3

all_tags = (
    "position",
    "album",
    "album_url",
    "cover_url",
    "artist",
    "year",
    "qwr",
    "average_rating",
    "user_ratings",
    "reviews",
    "score_distribution",
)

album_list = {
    "position": {
        "tag": "td",
        "subtag": {
            "tag": "strong",
        },
        "type": "int",
    },
    "album": {
        "tag": "a",
        "number": 0,
        "contains": {
            "album_url": {
                "key": "href",
                "type": "str",
            },
        },
        "type": "str",
    },
    "cover_url": {
        "tag": "img",
        "key": "src",
        "type": "str",
    },
    "artist": {
        "tag": "a",
        "number": 1,
        "contains": {
            "artist_url": {
                "key": "href",
                "type": "str",
            },
        },
        "type": "str",
    },
    "year": {
        "tag": "br",
        "number": 1,
        "match": r"\d{4}",
        "type": "int",
    },
    "qwr": {
        "tag": "div",
        "number": 1,
        "replace": {"QWR = ": ""},
        "type": "float",
    },
    "average_rating": {
        "tag": "span",
        "type": "float",
    },
    "user_ratings": {
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
    },
}
