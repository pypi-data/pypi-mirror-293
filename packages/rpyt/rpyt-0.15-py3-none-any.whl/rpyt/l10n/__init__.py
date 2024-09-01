import os
import re
from importlib.resources import files
from typing import Any, cast

from rpyt.common import (
    DIALOGUE_TAB,
    GAME_DIR,
    GAME_TL_DIR,
    GAME_TL_NONE_COMMON_RPYM,
    RENPY_COMMON_DIR,
    RENPY_COMMON_NAME,
    RENPY_RPY_EXT,
    RENPY_RPYM_EXT,
    hash_object,
    load_from_module,
    read_tab,
    rreplace,
)
from rpyt.l10n.common import TlString
from rpyt.l10n.processors import Processor

RESOURCES_COMMON_FILE = str(
    files("rpyt.resources").joinpath(
        f"{RENPY_COMMON_NAME}.{RENPY_RPYM_EXT}.txt"
    )
).replace("\\\\", "/")
LOCALES_DIR = "locales"
LOCALES_SRC_FILES_DIR = f"{LOCALES_DIR}/src"

DEFAULT_PROCESSOR = "rpyt.l10n.processors.JsonProcessor"

# g1 - file
# g2 - file line number
# g3 - string without quotes
TRANSLATE_STRINGS_OLD_PATTERN = r"^.*#\s(.+):(\d+)\n.*old\s['\"](.*)['\"]$"


DIALOGUE_STRING_TEMPLATE = """# {file}:{line}
translate {language} {identifier}:

{indent}# {old_renpy_script}
{indent}{new_renpy_script}
"""

STANDARD_STRING_LABEL_TEMPLATE = "translate {language} strings:\n"

STANDARD_STRING_TEMPLATE = """{indent}# {file}:{line}
{indent}old "{old}"
{indent}new "{new}"
"""


def read_common_rpym(file=GAME_TL_NONE_COMMON_RPYM):
    if not os.path.exists(file):
        file = RESOURCES_COMMON_FILE
    with open(file, encoding="utf-8") as fo:
        common = fo.read()
    matches: list[tuple[str, str, str]] = re.findall(
        TRANSLATE_STRINGS_OLD_PATTERN, common, re.MULTILINE
    )
    tlstrings: dict[str, TlString] = {}
    for cfile, lineno, ostring in matches:
        tlstring = TlString(None, None, ostring, cfile, int(lineno), None)
        hashid = hash_object(tuple(tlstring))
        if hashid not in tlstrings:
            tlstrings[hashid] = tlstring
    return tlstrings


def read_dialogue_tab(file=DIALOGUE_TAB):
    rows = read_tab(file, "header")
    rows.pop(0)
    tlstrings = dict(
        map(
            lambda e: (hash_object(tuple(e)), TlString(*e)),
            rows,
        )
    )
    return tlstrings


def get_src_file_name(tlstring: TlString) -> str:
    file = tlstring.filename
    if file.startswith(RENPY_COMMON_DIR):
        file = RENPY_COMMON_NAME
    else:
        file = file.removeprefix(GAME_DIR + "/")
        rpym_suffix, rpy_suffix = "." + RENPY_RPYM_EXT, "." + RENPY_RPY_EXT
        if file.endswith(rpym_suffix):
            file = file.removesuffix(rpym_suffix)
        elif file.endswith(rpy_suffix):
            file = file.removesuffix(rpy_suffix)
    return file


type ProcessorLike = type[Processor] | Processor | str


def get_processor(processor_like: ProcessorLike, **kwargs: Any):
    if isinstance(processor_like, str):
        processor = cast(type[Processor], load_from_module(processor_like))
    elif isinstance(processor_like, Processor):
        return processor_like
    return processor(**kwargs)


def get_src_files(
    tlstrings: dict[str, TlString],
    processor: ProcessorLike = DEFAULT_PROCESSOR,
    **kwargs: Any,
):
    processor = get_processor(processor, **kwargs)

    files: dict[str, dict[str, Any]] = {}

    for hashid, tlstring in tlstrings.items():
        file = f"{get_src_file_name(tlstring)}.{processor.extension}"
        if file not in files:
            content = files[file] = {}
        else:
            content = files[file]
        content[hashid] = processor.process(hashid, tlstring)

    return files


def make_src_files(
    dir=LOCALES_SRC_FILES_DIR,
    dialogue_tab=DIALOGUE_TAB,
    common_rpym=GAME_TL_NONE_COMMON_RPYM,
    processor: ProcessorLike = DEFAULT_PROCESSOR,
    **kwargs: Any,
):
    processor = get_processor(processor, **kwargs)
    tlstrings = {
        **read_common_rpym(common_rpym),
        **read_dialogue_tab(dialogue_tab),
    }

    files = dict(
        map(
            lambda e: (f"{dir}/{e[0]}", e[1]),
            get_src_files(tlstrings, processor).items(),
        )
    )

    if files:
        os.makedirs(dir, exist_ok=True)

    totstrs = 0
    for file, content in files.items():
        dirname = os.path.dirname(file)
        os.makedirs(dirname, exist_ok=True)
        processor.write(file, content)
        totstrs += len(content)
        print(f"dumped {len(content)} string(s) into '{file}'")

    print(f"created {len(files)} file(s); dumped {totstrs} string(s)")


def get_tl_file(
    file: str,
    language: str,
    tlstrings: dict[str, TlString],
    indent=4,
    processor: ProcessorLike = DEFAULT_PROCESSOR,
    **kwargs: Any,
):
    processor = get_processor(processor, **kwargs)
    strings = processor.read(file)

    standard_strings: dict[TlString, str] = {}

    rv: list[str] = []
    for hashid, string in strings.items():
        tlstring = tlstrings.get(hashid, None)
        if tlstring:
            if tlstring.identifier and tlstring.renpy_script:
                rv.append(
                    DIALOGUE_STRING_TEMPLATE.format(
                        file=tlstring.filename,
                        line=tlstring.line_number,
                        language=language,
                        identifier=tlstring.identifier,
                        old_renpy_script=rreplace(
                            tlstring.renpy_script,
                            "[what]",
                            tlstring.dialogue,
                            1,
                        ),
                        new_renpy_script=rreplace(
                            tlstring.renpy_script,
                            "[what]",
                            string,
                            1,
                        ),
                        indent=" " * indent,
                    )
                )
            else:
                standard_strings[tlstring] = string

    if standard_strings:
        rv.append(STANDARD_STRING_LABEL_TEMPLATE.format(language=language))

    for tlstring, string in standard_strings.items():
        if (not tlstring.identifier) and (not tlstring.renpy_script):
            rv.append(
                STANDARD_STRING_TEMPLATE.format(
                    file=tlstring.filename,
                    line=tlstring.line_number,
                    old=tlstring.dialogue,
                    new=string,
                    indent=" " * indent,
                )
            )

    return "\n".join(rv)


def get_tl_files(
    dir: str,
    language: str,
    tlstrings: dict[str, TlString],
    indent=4,
    processor: ProcessorLike = DEFAULT_PROCESSOR,
    **kwargs: Any,
):
    processor = get_processor(processor, **kwargs)

    rv: dict[str, str] = {}
    for dirpath, _, filenames in os.walk(dir):
        rdirpath = dirpath.replace("\\", "/")[len(f"{dir}/") :]
        for filename in filenames:
            suffix = "." + processor.extension
            if filename.endswith(suffix):
                file = (rdirpath + "/" if rdirpath else "") + rreplace(
                    filename, suffix, "." + RENPY_RPY_EXT, 1
                )
                rv[file] = get_tl_file(
                    f"{dirpath}/{filename}",
                    language,
                    tlstrings,
                    indent,
                    processor,
                    **kwargs,
                )

    return rv


def make_tl_files(
    src_dir: str,
    language: str,
    tl_dir=GAME_TL_DIR,
    indent=4,
    dialogue_tab=DIALOGUE_TAB,
    common_rpym=GAME_TL_NONE_COMMON_RPYM,
    processor: ProcessorLike = DEFAULT_PROCESSOR,
    **kwargs: Any,
):
    processor = get_processor(processor, **kwargs)
    tlstrings = {
        **read_common_rpym(common_rpym),
        **read_dialogue_tab(dialogue_tab),
    }
    tl_dir += "/" + language
    files = dict(
        map(
            lambda e: (f"{tl_dir}/{e[0]}", e[1]),
            get_tl_files(
                src_dir, language, tlstrings, indent, processor, **kwargs
            ).items(),
        )
    )

    if files:
        os.makedirs(tl_dir, exist_ok=True)

    for file, content in files.items():
        dirname = os.path.dirname(file)
        os.makedirs(dirname, exist_ok=True)
        with open(file, "w", encoding="utf-8") as fo:
            fo.write(content)
        print(f"dumped translated strings into '{file}'")

    print(f"created {len(files)} file(s)")
