import json
from io import TextIOWrapper
from typing import Any

from rpyt.l10n.common import TlString
from rpyt.l10n.processors.processor import Processor


class JsonProcessor(Processor):
    extension = "json"

    def __init__(self, indent=4):
        self.indent = indent

    def read(self, file: str) -> dict[str, str]:
        with open(file, encoding="utf-8") as fo:
            return json.load(fo)

    def write(
        self, file: str | TextIOWrapper, content: dict[str, Any]
    ) -> None:
        file = (
            open(file, "w", encoding="utf-8")
            if isinstance(file, str)
            else file
        )
        json.dump(content, file, indent=self.indent)
        file.close()

    def process(self, hashid: str, tlstring: TlString) -> str:
        return tlstring.dialogue
