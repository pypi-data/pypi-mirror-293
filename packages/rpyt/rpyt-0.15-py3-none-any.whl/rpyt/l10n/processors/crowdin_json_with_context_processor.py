import json
import re
from typing import Any, NotRequired, TypedDict, cast

from rpyt.l10n.common import TlString
from rpyt.l10n.processors.json_processor import JsonProcessor


# as specified in: https://crowdin.com/store/apps/json-with-context
class Data(TypedDict):
    text: str
    crowdinContext: str


class Context(TypedDict):
    content: str
    values: NotRequired[dict[str, dict[str, Any]]]


class Contexts(TypedDict):
    standard: Context
    dialogue: Context


class CrowdinJsonWithContextProcessor(JsonProcessor):
    def __init__(self, contexts_json: str | None = None, **kwargs: Any):
        super().__init__(**kwargs)
        if contexts_json:
            with open(contexts_json, encoding="utf-8") as fo:
                self.contexts = Contexts(**json.load(fo))
        else:
            self.contexts = None

    def read(self, file: str) -> dict[str, str]:
        rv = super().read(file)
        for hashid, content in rv.items():
            if isinstance(content, dict):
                content = cast(Data, content)
                rv[hashid] = content["text"]
            else:
                pass
        return rv

    def process(self, hashid: str, tlstring: TlString):
        ctx: Context | None = (
            (
                self.contexts["dialogue"]
                if tlstring.identifier
                else self.contexts["standard"]
            )
            if self.contexts
            else None
        )
        if not ctx:
            return super().process(hashid, tlstring)
        return Data(
            text=tlstring.dialogue,
            crowdinContext=ctx["content"].format(
                **self.get_values(tlstring, ctx.get("values", {}))
            ),
        )

    def get_values(
        self, tlstring: TlString, values: dict[str, dict[str, Any]]
    ):
        tlstr = tlstring._asdict()
        for k, v in tlstr.items():
            if k in values:
                key = next(
                    filter(lambda e: re.search(e, str(v)), values[k]), None
                )
                if key:
                    aval = values[k][key]
                    tlstr[k] = (
                        str.format(aval, **tlstr)
                        if isinstance(aval, str)
                        else aval
                    )
        return tlstr
