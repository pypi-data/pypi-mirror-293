import mimetypes
from pathlib import Path
from urllib.parse import urljoin, urlparse


def get_pathname(url: str) -> Path:
    return Path(urlparse(url).path)


def get_filename(url: str) -> str | None:
    if mimetypes.guess_type(url, strict=True)[0]:
        url_pathname = Path(urlparse(url).path)
        return url_pathname.name

    return None


def strip_qs(url: str) -> str:
    return urljoin(url, urlparse(url).path)
