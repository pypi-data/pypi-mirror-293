from collections.abc import Callable

from gaveta.utils import T


def replace_or_append(
    values: list[T], new_value: T, key: Callable[[T, T], bool]
) -> list[T]:
    for index, value in enumerate(values):
        if key(value, new_value):
            values[index] = new_value
            break
    else:
        values.append(new_value)

    return values
