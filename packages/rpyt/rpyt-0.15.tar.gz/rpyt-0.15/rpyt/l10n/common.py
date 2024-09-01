from typing import NamedTuple


class TlString(NamedTuple):
    identifier: str | None
    character: str | None
    dialogue: str
    filename: str
    line_number: int
    renpy_script: str | None
