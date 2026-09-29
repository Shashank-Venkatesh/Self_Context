"""Convert fetched HTML pages into readable normalized web records."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from html.parser import HTMLParser
from typing import Any
from urllib.parse import urldefrag, urlparse, urlunparse

from .models import NormalizedWebPage

_SKIP_TAGS = {"script", "style", "noscript", "template", "head"}


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.title_parts: list[str] = []
        self._skip_depth = 0
        self._in_title = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in _SKIP_TAGS:
            self._skip_depth += 1
        elif tag == "title":
            self._in_title = True
        elif tag in ("p", "div", "br", "li", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "section", "article"):
            self.parts.append("\n")

    def handle_endtag(self, tag: str) -> None:
        if tag in _SKIP_TAGS and self._skip_depth > 0:
            self._skip_depth -= 1
        elif tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title_parts.append(data)
        if self._skip_depth == 0 and not self._in_title:
            self.parts.append(data)

    def text(self) -> str:
        joined = " ".join(self.parts)
        return re.sub(r"[ \t]*\n[ \t]*", "\n", re.sub(r"\s+", " ", joined)).strip()

    def title(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.title_parts)).strip()


def extract_text(html: str) -> tuple[str, str]:
    """Extract (text, title) from an HTML document."""
    parser = _TextExtractor()
    parser.feed(html)
    return parser.text(), parser.title()


def canonicalize_url(url: str) -> str:
    """Canonicalize a URL: lowercase scheme/host, drop fragment and default port."""
    without_fragment, _ = urldefrag(url)
    parsed = urlparse(without_fragment)
    scheme = (parsed.scheme or "https").lower()
    hostname = (parsed.hostname or "").lower()
    port = parsed.port
    netloc = hostname
    if port and not (scheme == "http" and port == 80) and not (scheme == "https" and port == 443):
        netloc = f"{hostname}:{port}"
    path = parsed.path or "/"
    return urlunparse((scheme, netloc, path, "", parsed.query, ""))


def normalize_web_page(page: dict[str, Any]) -> NormalizedWebPage:
    text, title = extract_text(page.get("html", ""))
    final_url = page.get("final_url") or page["url"]
    return NormalizedWebPage(
        url=page["url"],
        canonical_url=canonicalize_url(final_url),
        title=title or final_url,
        text=text,
        fetched_at=datetime.now(timezone.utc),
        metadata={"content_type": page.get("content_type", ""), "requested_url": page["url"]},
    )
