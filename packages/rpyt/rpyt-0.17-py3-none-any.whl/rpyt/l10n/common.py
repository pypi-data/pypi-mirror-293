from typing import NamedTuple

L10N_DIR = "l10n"


class TlString(NamedTuple):
    identifier: str | None
    character: str | None
    dialogue: str
    filename: str
    line_number: int
    renpy_script: str | None
