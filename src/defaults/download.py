#!/usr/bin/env python3

AOTY_TYPES = ("LP", "EP", "Mixtape", "Compilation", "Live", "Soundtrack")
PROG_TYPES = {
    "Studio": 1,
    "DVD": 2,
    "Boxset,Compilation": 3,
    "Live": 4,
    "Singles,EPs,FanClub,Promo": 5,
}
PROG_GENRES = {
    "Canterbury Scene": 12,
    "Crossover Prog": 3,
    "Eclectic Prog": 42,
    "Experimental/Post Metal": 44,
    "Heavy Prog": 41,
    "Indo-Prog/Raga Rock": 35,
    "Jazz Rock/Fusion": 30,
    "Krautrock": 17,
    "Neo-Prog": 18,
    "Post Rock/Math Rock": 32,
    "Prog Folk": 6,
    "Progressive Electronic": 33,
    "Progressive Metal": 19,
    "Psychedelic/Space Rock": 15,
    "RIO/Avant-Prog": 36,
    "Rock Progressivo Italiano": 28,
    "Symphonic Prog": 4,
    "Tech/Extreme Prog Metal": 43,
    "Zeuhl": 11,
    "Various Genres/Artists": 29,
    "Prog Related": 38,
    "Proto-Prog": 37,
}

AOTY_MAX_SCORE = 100
AOTY_MIN_SCORE = 83
PROG_MAX_SCORE = 5.0
PROG_MIN_SCORE = 3.95
