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
        if isinstance(file, str):
            ocontent = content
            # try to recover the existing strings if possible
            try:
                strings = self.read(file)
                content = content.copy()
                recovered = 0
                for key in content:
                    new = self.update(content[key], strings.get(key))
                    recovered += 1 if new != content[key] else 0
                    content[key] = new
                print(
                    f"recovered {recovered} string(s) from existing '{file}'"
                )
            except Exception:
                print(
                    f"failed to recover strings from existing '{file}', overwriting instead"
                )
                content = ocontent
        file = (
            open(file, "w", encoding="utf-8")
            if isinstance(file, str)
            else file
        )
        json.dump(content, file, indent=self.indent)
        file.close()

    def process(self, hashid: str, tlstring: TlString) -> str:
        return tlstring.dialogue

    def update(self, old: str, new: str | None) -> str:
        return new if new is not None else old
