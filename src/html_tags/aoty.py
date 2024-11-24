#!/usr/bin/env python3

albumlist = {
    "position": {
        "tag": "span",
        "class": "albumListRank",
        "subtag": {
            "tag": "span",
        },
        "type": "int",
    },
    "title": {
        "tag": "h2",
        "class": "albumListTitle",
        "type": "str",
        "subtag": {
            "tag": "a",
        },
        "contains": {
            "album_url": {
                "key": "href",
                "type": "str",
            },
        },
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
        "replace": {
            ",": ""
        },
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
                "replace": {
                    " Ratings": "",
                },
                "type": "int",
            }
        }
    },
}
