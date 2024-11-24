from pathlib import Path

PROG_NAME = "MusicLists"
VERSION = "0.1"

HEADERS_COLOR = "yellow"
OPTIONS_COLOR = "green"

DL_CHOICES = ("all", "aoty", "prog", "none")
AOTY_TYPES = ("LP", "EP", "Mixtape", "Compilation", "Live", "Soundtrack")
PROG_TYPES = (
    "Studio", "DVD", "Boxset,Compilation", "Live", "Singles,EPs,FanClub,Promo"
)

VERBOSE = False
DEBUG = False

TEXT = False
DEDUP = True
ONLY_HIGHEST_MATCH = True

INCLUDE_URL = False
INCLUDE_TRACKS = False

AOTY_MAX_SCORE = 100
AOTY_MIN_SCORE = 83
PROG_MAX_SCORE = 5.0
PROG_MIN_SCORE = 3.95

KEY_LENGTH = 14
KEY_SEP = "-"

AUTO_FIELD = "possible"
VERIFIED_FIELD = "verified"
SUFFIX = "json"
TEXT_SUFFIX = "txt"

MIN_LEVEL = 1
MAX_LEVEL = 4

CURRENT_DIR = Path(__file__).parent
SRC_DIR = CURRENT_DIR.parent
ROOT_DIR = SRC_DIR.parent
LIST_DIR = Path(ROOT_DIR / "lists")
JSON_DIR = Path(LIST_DIR / "json")
TXT_DIR = Path(LIST_DIR / "txt")
DEDUP_DIR = Path(ROOT_DIR / "dedup")
DIRS = (
    LIST_DIR,
    JSON_DIR,
    TXT_DIR
)  # type: tuple[Path, ...]
for d in DIRS:
    d.mkdir(exist_ok=True)

AOTY_PATH = Path(JSON_DIR / f"aoty.{SUFFIX}")
PROG_PATH = Path(JSON_DIR / f"prog.{SUFFIX}")
MERGE_PATH = Path(JSON_DIR / f"merge.{SUFFIX}")
DIRS_PATH = Path(JSON_DIR / f"dirs.{SUFFIX}")
WANTED_PATH = Path(JSON_DIR / f"wanted.{SUFFIX}")
LEFTOVER_PATH = Path(JSON_DIR / f"leftover.{SUFFIX}")

AOTY_TEXT_PATH = Path(TXT_DIR / f"aoty.{TEXT_SUFFIX}")
PROG_TEXT_PATH = Path(TXT_DIR / f"prog.{TEXT_SUFFIX}")
MERGE_TEXT_PATH = Path(TXT_DIR / f"merge.{TEXT_SUFFIX}")
DIRS_TEXT_PATH = Path(TXT_DIR / f"dirs.{TEXT_SUFFIX}")
WANTED_TEXT_PATH = Path(TXT_DIR / f"wanted.{TEXT_SUFFIX}")
LEFTOVER_TEXT_PATH = Path(TXT_DIR / f"leftover.{TEXT_SUFFIX}")
