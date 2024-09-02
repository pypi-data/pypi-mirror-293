import json
from enum import Enum
from pathlib import Path
from typing import Any

from gaveta.files import ensure_dir
from gaveta.utils import assert_never


class EOF(Enum):
    NL = 1
    DEFAULT = 2


class Starter(Enum):
    ARRAY = 1
    OBJECT = 2


def read_json(input_path: Path) -> Any:  # noqa: ANN401
    with input_path.open(mode="r") as f:
        return json.load(f)


def write_json(
    data: Any,  # noqa: ANN401
    output_path: Path,
    indent: int = 2,
    eof: EOF = EOF.NL,
) -> None:
    with output_path.open(mode="w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

        match eof:
            case EOF.NL:
                f.write("\n")
            case EOF.DEFAULT:
                pass
            case _:
                assert_never(eof)


def ensure_json(file: Path, starter: Starter = Starter.ARRAY) -> None:
    if not file.is_file():
        ensure_dir(file.parent)

        match starter:
            case Starter.ARRAY:
                write_json([], file)
            case Starter.OBJECT:
                write_json({}, file)
            case _:
                assert_never(starter)
