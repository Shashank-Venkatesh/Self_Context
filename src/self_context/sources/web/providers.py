"""Web provider interfaces and a domain-filtered HTTP implementation."""

from __future__ import annotations

import re
import urllib.error
import urllib.request
from collections.abc import Iterable
from typing import Any, Protocol
from urllib.parse import urlparse

USER_AGENT = "self-context/0.1 (+https://github.com/self-context; personal context indexer)"
DEFAULT_TIMEOUT = 30.0


class WebProvider(Protocol):
    def fetch_pages(self, urls: Iterable[str]) -> Iterable[dict[str, Any]]: ...
    def fetch_page(self, url: str) -> dict[str, Any]: ...


def normalize_domain(domain: str) -> str:
    """Validate and normalize a domain for the allowlist."""
    normalized = domain.strip().lower()
    normalized = re.sub(r"^https?://", "", normalized).split("/")[0].split(":")[0]
    if not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+", normalized):
        raise ValueError(f"Invalid domain: {domain}")
    return normalized


def is_allowed(url: str, domains: Iterable[str]) -> bool:
    """Return True when the URL hostname matches an allowed domain or a subdomain of it."""
    hostname = (urlparse(url).hostname or "").lower()
    if not hostname:
        return False
    return any(hostname == domain or hostname.endswith(f".{domain}") for domain in domains)


class HttpWebProvider:
    """Fetches pages over HTTP, restricted to an explicit domain allowlist."""

    def __init__(self, allowed_domains: Iterable[str], timeout: float = DEFAULT_TIMEOUT,
                 user_agent: str = USER_AGENT):
        self.allowed_domains = tuple(normalize_domain(d) for d in allowed_domains)
        if not self.allowed_domains:
            raise ValueError("At least one allowed domain is required.")
        self.timeout = timeout
        self.user_agent = user_agent
        self.skipped: list[str] = []

    def fetch_pages(self, urls: Iterable[str]) -> Iterable[dict[str, Any]]:
        for url in urls:
            page = self.fetch_page(url)
            if page is not None:
                yield page

    def fetch_page(self, url: str) -> dict[str, Any] | None:
        if not is_allowed(url, self.allowed_domains):
            self.skipped.append(url)
            return None
        request = urllib.request.Request(url, headers={"User-Agent": self.user_agent})
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                content_type = response.headers.get("Content-Type", "")
                charset = response.headers.get_content_charset() or "utf-8"
                body = response.read().decode(charset, errors="replace")
                final_url = response.geturl()
        except urllib.error.URLError as error:
            raise RuntimeError(f"Failed to fetch {url}: {error}") from error
        return {
            "url": url,
            "final_url": final_url,
            "content_type": content_type,
            "html": body,
        }
