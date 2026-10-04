"""Retrieval service that keeps callers independent of the storage engine."""

from .models import ContextItem
from .storage import ContextStore


class RetrievalService:
    def __init__(self, store: ContextStore):
        self.store = store

    def search_context(self, query: str, source: str | None = None,
                       type: str | None = None) -> list[ContextItem]:
        return self.store.search(query, source=source, type=type)

    def get_context_item(self, item_id: str) -> ContextItem | None:
        return self.store.get(item_id)

    def list_items(self, source: str | None = None, type: str | None = None,
                   limit: int = 20) -> list[ContextItem]:
        return self.store.list_items(source=source, type=type, limit=limit)

    def search_emails(self, query: str) -> list[ContextItem]:
        return self.search_context(query, source="email")

    def search_web(self, query: str) -> list[ContextItem]:
        return self.search_context(query, source="web")