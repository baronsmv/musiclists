#!/usr/bin/env python3

albumlist = {
    "position": {
        "tag": "td",
        "subtag": {
            "tag": "strong",
        },
        "type": "int",
    },
    "cover_url": {
        "tag": "img",
        "type": "str",
        "key": "src",
    },
    "average_rating": {
        "tag": "span",
        "type": "float",
    },
    "ratings": {
        "tag": "span",
        "type": "int",
        "number": 1,
    },
    "qwr": {
        "tag": "div",
        "type": "float",
        "number": 1,
        "replace": {"QWR = ": ""},
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
}
album = {
    "title": {
        "tag": "div",
        "class": "albumTitle",
        "type": "str",
        "subtag": {
            "tag": "span",
        },
    },
    "cover_url": {
        "tag": "div",
        "class": "albumTopBox cover",
        "type": "str",
        "subtag": {
            "tag": "img",
        },
        "key": "src",
    },
    "artist": {
        "tag": "div",
        "class": "artist",
        "type": "str",
        "subtag": {
            "tag": "a",
        },
        "contains": {
            "artist_url": {
                "key": "href",
                "type": "str",
            },
        },
    },
    "critic_score": {
        "tag": "div",
        "class": "albumCriticScore",
        "type": "int",
        "subtag": {
            "tag": "a",
        },
    },
    "critic_reviews": {
        "tag": "div",
        "class": "text numReviews",
        "type": "int",
        "subtag": {
            "tag": "span",
        },
    },
    "user_score": {
        "tag": "div",
        "class": "albumUserScore",
        "type": "int",
        "subtag": {
            "tag": "a",
        },
    },
    "user_reviews": {
        "tag": "div",
        "class": "albumUserScoreBox",
        "type": "int",
        "subtag": {
            "tag": "strong",
        },
        "replace": {",": ""},
    },
    "year": {
        "tag": "div",
        "class": "detailRow",
        "type": "int",
        "subtag": {
            "tag": "a",
            "number": -1,
        },
    },
    "month": {
        "tag": "div",
        "class": "detailRow",
        "type": "str",
        "subtag": {
            "tag": "a",
            "number": -2,
        },
    },
    "day": {
        "tag": "div",
        "class": "detailRow",
        "type": "str",
        "match": r"(\d+)",
    },
    "genres": {
        "tag": "div",
        "class": "detailRow",
        "number": 3,
        "type": "list",
        "expand": "a",
        "expand_url": "genre",
    },
    "labels": {
        "tag": "div",
        "class": "detailRow",
        "number": 2,
        "type": "list",
        "expand": "a",
        "expand_url": "label",
    },
    "producers": {
        "tag": "div",
        "class": "detailRow",
        "number": 4,
        "type": "list",
        "expand": "a",
        "expand_url": "producer",
    },
    "writers": {
        "tag": "div",
        "class": "detailRow",
        "number": 5,
        "type": "list",
        "expand": "a",
        "expand_url": "writer",
    },
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
