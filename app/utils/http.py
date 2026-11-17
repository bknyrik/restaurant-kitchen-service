import unicodedata
from urllib.parse import urlsplit

from flask import request


def url_has_allowed_host_and_scheme(url: str) -> bool:
    if not url:
        return False

    url_info = urlsplit(url)

    if url_info.scheme and not url_info.netloc:
        return False

    if unicodedata.category(url[0])[0] == "C":
        return False

    scheme = url_info.scheme

    if not scheme and url_info.netloc:
        scheme = "https"

    return (
        not url_info.netloc
        or (
            bool(request.trusted_hosts)
            and url_info.netloc in request.trusted_hosts
        )
        and (not scheme or scheme in ("http", "https"))
    )
