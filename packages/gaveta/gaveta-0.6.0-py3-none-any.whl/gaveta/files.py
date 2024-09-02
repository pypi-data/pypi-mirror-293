from pathlib import Path


def ensure_dir(folder: Path) -> None:
    folder.mkdir(parents=True, exist_ok=True)
