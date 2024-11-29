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
    "user_score": {
        "tag": "div",
        "number": 1,
        "replace": {"QWR = ": ""},
        "type": "float",
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
