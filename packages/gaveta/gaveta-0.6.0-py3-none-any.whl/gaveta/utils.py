from typing import NoReturn, TypeVar

T = TypeVar("T")


def assert_never(value: NoReturn) -> NoReturn:
    msg = f"Unsupported value: {value} ({type(value).__name__})"
    raise AssertionError(msg)
