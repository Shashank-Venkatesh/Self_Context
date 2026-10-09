"""Web ingestion pipeline: fetch, normalize, map, and idempotently persist."""

from __future__ import annotations

from collections.abc import Iterable

from ...core.models import ContextItem, utc_now
from ...core.storage import ContextStore
from .normalization import normalize_web_page
from .providers import WebProvider


class WebIngestor:
    def __init__(self, provider: WebProvider, store: ContextStore):
        self.provider = provider
        self.store = store

    def sync(self, urls: Iterable[str]) -> int:
        count = 0
        for raw_page in self.provider.fetch_pages(urls):
            normalized = normalize_web_page(raw_page)
            now = utc_now()
            item = ContextItem(
                id=f"web:{normalized.canonical_url}", source="web", source_id=normalized.canonical_url,
                type="web", title=normalized.title, content=normalized.text,
                metadata={"url": normalized.url, "canonical_url": normalized.canonical_url,
                          **normalized.metadata},
                created_at=normalized.fetched_at, updated_at=normalized.fetched_at, indexed_at=now,
            )
            self.store.add(item)
            count += 1
        return count
