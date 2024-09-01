import hashlib
from importlib import import_module
from typing import Any, Literal

RENPY_COMMON_NAME = "common"
RENPY_RPY_EXT = "rpy"
RENPY_RPYM_EXT = f"{RENPY_RPY_EXT}m"
RENPY_COMMON_DIR = f"renpy/{RENPY_COMMON_NAME}"
GAME_DIR = "game"
GAME_TL_DIR = f"{GAME_DIR}/tl"
GAME_TL_NONE_COMMON_RPYM = (
    f"{GAME_TL_DIR}/None/{RENPY_COMMON_NAME}.{RENPY_RPYM_EXT}"
)
DIALOGUE_TAB = "dialogue.tab"


def hash_object(obj: Any, length=8):
    # Convert the tuple to a string representation
    tuple_string = str(obj)

    # Create a SHA-256 hash of the string
    sha = hashlib.sha256(tuple_string.encode())

    # Convert the hash to a hexadecimal string and take the first 8 characters
    hash_hex = sha.hexdigest()[:length]

    return hash_hex


def read_tab(
    file: str, normalize_column: Literal["header", "max"] | None = None
):
    with open(file, encoding="utf-8") as fo:
        rows = [(tuple(ln.split("\t"))) for ln in fo.read().splitlines()]
    mx_col_count = max(map(len, rows))
    hd_col_count = len(rows[0])
    rv: list[tuple[Any, ...]] = []
    for row in rows:
        nrow: list[Any] = []
        for col in row:
            try:
                nrow.append(int(col))
                continue
            except Exception:
                pass
            try:
                nrow.append(float(col))
                continue
            except Exception:
                pass
            if not col:
                nrow.append(None)
                continue
            else:
                nrow.append(col)
        if normalize_column is not None:
            target = (
                hd_col_count if normalize_column == "header" else mx_col_count
            )
            nrow += [None] * (target - len(nrow))
        rv.append(tuple(nrow))
    return rv


def rreplace(string: str, old: str, new: str, count=-1):
    return new.join(string.rsplit(old, count))


def load_from_module(string: str):
    module, _, name = string.rpartition(".")
    return getattr(import_module(module), name)
