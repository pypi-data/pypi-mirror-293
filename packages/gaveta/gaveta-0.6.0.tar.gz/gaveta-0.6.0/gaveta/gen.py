from uuid import uuid4


def new_id(prefix: str) -> str:
    copyable_id = str(uuid4()).replace("-", "")

    return f"{prefix}_{copyable_id}"
