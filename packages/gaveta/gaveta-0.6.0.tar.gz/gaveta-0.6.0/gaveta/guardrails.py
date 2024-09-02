from gaveta.utils import T


def require_value(value: T | None) -> T:
    if value is None:
        msg = "Value must not be None"
        raise ValueError(msg)

    return value
