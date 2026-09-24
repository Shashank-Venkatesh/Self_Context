"""Email ingestion pipeline: fetch, normalize, map, and idempotently persist."""

from __future__ import annotations

from ...core.models import ContextItem, utc_now
from ...core.storage import ContextStore
from .normalization import normalize_gmail_message
from .providers import EmailProvider


class EmailIngestor:
    def __init__(self, provider: EmailProvider, store: ContextStore):
        self.provider = provider
        self.store = store

    def sync(self, query: str | None = None) -> int:
        count = 0
        for raw_message in self.provider.fetch_messages(query):
            normalized = normalize_gmail_message(raw_message)
            now = utc_now()
            item = ContextItem(
                id=f"email:{normalized.message_id}", source="email", source_id=normalized.message_id,
                type="email", title=normalized.subject, content=normalized.body,
                metadata={"thread_id": normalized.thread_id, "sender": normalized.sender,
                          "recipients": normalized.recipients, "cc": normalized.cc,
                          "bcc": normalized.bcc, "labels": normalized.labels},
                created_at=normalized.timestamp, updated_at=normalized.timestamp, indexed_at=now,
            )
            self.store.add(item)
            count += 1
        return count