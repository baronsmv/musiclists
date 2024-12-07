#!/usr/bin/env python3

all_tags = (
    "position",
    "album",
    "album_url",
    "cover_url",
    "artist",
    "critic_score",
    "critic_reviews",
    "user_score",
    "user_ratings",
    "year",
    "month",
    "day",
    "genre",
    "labels",
    "producers",
    "writers",
    "track_disc",
    "track_number",
    "track_title",
    "track_url",
    "sub_tracks",
    "track_length",
    "featuring",
    "track_score",
    "track_ratings",
)

album_list = {
    "position": {
        "tag": "span",
        "class": "albumListRank",
        "subtag": {
            "tag": "span",
        },
        "type": "int",
    },
    "album": {
        "tag": "h2",
        "class": "albumListTitle",
        "subtag": {
            "tag": "a",
        },
        "contains": {
            "album_url": {
                "key": "href",
                "type": "str",
            },
        },
        "type": "str",
    },
}
album = {
    "album": {
        "tag": "div",
        "class": "albumTitle",
        "subtag": {
            "tag": "span",
        },
        "type": "str",
    },
    "cover_url": {
        "tag": "div",
        "class": "albumTopBox cover",
        "subtag": {
            "tag": "img",
        },
        "key": "src",
        "type": "str",
    },
    "artist": {
        "tag": "div",
        "class": "artist",
        "subtag": {
            "tag": "span",
        },
        "contains": {
            "artist_url": {
                "tag": "a",
                "key": "href",
                "type": "str",
            },
        },
        "type": "str",
    },
    "critic_score": {
        "tag": "div",
        "class": "albumCriticScore",
        "subtag": {
            "tag": "a",
        },
        "type": "int",
    },
    "critic_reviews": {
        "tag": "div",
        "class": "text numReviews",
        "subtag": {
            "tag": "span",
        },
        "type": "int",
    },
    "user_score": {
        "tag": "div",
        "class": "albumUserScore",
        "subtag": {
            "tag": "a",
        },
        "type": "int",
    },
    "user_ratings": {
        "tag": "div",
        "class": "albumUserScoreBox",
        "subtag": {
            "tag": "strong",
        },
        "replace": {",": ""},
        "type": "int",
    },
    "year": {
        "tag": "div",
        "class": "detailRow",
        "subtag": {
            "tag": "a",
            "number": -1,
        },
        "type": "int",
    },
    "month": {
        "tag": "div",
        "class": "detailRow",
        "subtag": {
            "tag": "a",
            "number": -2,
        },
        "type": "str",
    },
    "day": {
        "tag": "div",
        "class": "detailRow",
        "match": r"(\d+)",
        "type": "str",
    },
    "genre": {
        "tag": "div",
        "class": "detailRow",
        "number": 3,
        "expand": "a",
        "expand_url": "genre",
        "type": "list",
    },
    "labels": {
        "tag": "div",
        "class": "detailRow",
        "number": 2,
        "expand": "a",
        "expand_url": "label",
        "type": "list",
    },
    "producers": {
        "tag": "div",
        "class": "detailRow",
        "number": 4,
        "expand": "a",
        "expand_url": "producer",
        "type": "list",
    },
    "writers": {
        "tag": "div",
        "class": "detailRow",
        "number": 5,
        "expand": "a",
        "expand_url": "writer",
        "type": "list",
    },
}
tracklist = {
    "track_disc": {
        "tag": "div",
        "class": "discNumber",
        "type": "str",
    },
    "track_number": {
        "tag": "td",
        "class": "trackNumber",
        "type": "int",
    },
    "track_title": {
        "tag": "td",
        "class": "trackTitle",
        "subtag": {
            "tag": "a",
        },
        "contains": {
            "track_url": {
                "key": "href",
                "type": "str",
            },
        },
        "type": "str",
    },
    "sub_tracks": {
        "tag": "div",
        "class": "trackNotes",
        "subtag": {
            "tag": "ul",
        },
        "expand": "li",
        "type": "list_str",
    },
    "track_length": {
        "tag": "div",
        "class": "length",
        "type": "str",
    },
    "featuring": {
        "tag": "div",
        "class": "featuredArtists",
        "expand": "a",
        "expand_url": "artist",
        "type": "list",
    },
    "track_score": {
        "tag": "td",
        "class": "trackRating",
        "subtag": {
            "tag": "span",
        },
        "contains": {
            "track_ratings": {
                "key": "title",
                "replace": {
                    " Ratings": "",
                },
                "type": "int",
            }
        },
        "type": "int",
    },
}
