import json
import re
from typing import Any, NotRequired, TypedDict, cast

from rpyt.l10n.common import TlString
from rpyt.l10n.processors.json_processor import JsonProcessor


class Template(TypedDict):
    key: str
    keys: list[str]
    values: NotRequired[dict[str, Any]]


class Context(TypedDict):
    values: NotRequired[dict[str, Any]]


class Contexts(TypedDict):
    template: Template
    standard: Context
    dialogue: Context


class DynamicJsonProcessor(JsonProcessor):
    def __init__(self, dynamic_json: str | None = None, **kwargs: Any):
        super().__init__(**kwargs)
        if dynamic_json:
            with open(dynamic_json, encoding="utf-8") as fo:
                self.dynamic = Contexts(**json.load(fo))
        else:
            self.dynamic = None

    def read(self, file: str) -> dict[str, str]:
        rv = super().read(file)
        if self.dynamic:
            for hashid, content in rv.items():
                if isinstance(content, dict):
                    content = cast(dict[str, Any], content)
                    rv[hashid] = content[self.dynamic["template"]["key"]]
                else:
                    pass
        return rv

    def process(self, hashid: str, tlstring: TlString):
        temp: Template | None = (
            self.dynamic["template"] if self.dynamic else None
        )
        ctx: Context | None = (
            (
                self.dynamic["dialogue"]
                if tlstring.identifier
                else self.dynamic["standard"]
            )
            if self.dynamic
            and "dialogue" in self.dynamic
            and "standard" in self.dynamic
            else None
        )
        if not temp or not ctx:
            return super().process(hashid, tlstring)
        values = self.get_values(
            tlstring, {**temp.get("values", {}), **ctx.get("values", {})}
        )
        return {key: values[key] for key in temp["keys"]}

    def get_values(self, tlstring: TlString, values: dict[str, Any]):
        vals = tlstring._asdict()
        sep = "."
        for key, val in values.items():
            pattern: str | None = None
            if sep in key:
                key, _, pattern = key.partition(sep)
            if (pattern is None) or (
                (pattern is not None) and re.search(pattern, str(vals[key]))
            ):
                vals[key] = val.format(**vals) if isinstance(val, str) else val
        return vals
