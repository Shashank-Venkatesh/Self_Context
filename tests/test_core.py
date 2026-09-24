from datetime import datetime, timezone

from self_context.core.models import ContextItem
from self_context.core.retrieval import RetrievalService


def item(item_id: str = "one", source: str = "notes") -> ContextItem:
    now = datetime.now(timezone.utc)
    return ContextItem(item_id, source, item_id, "note", "Project meeting", "Discussed machine learning", {"tag": "work"}, now, now, now)


def test_store_crud_and_duplicate_upsert(store):
    store.add(item())
    assert store.count() == 1
    assert store.get("one").title == "Project meeting"
    updated = item()
    updated.title = "Updated meeting"
    store.update(updated)
    assert store.get_by_source("notes", "one").title == "Updated meeting"
    store.add(item("one", "notes"))
    assert store.count() == 1
    assert store.delete("one") is True
    assert store.get("one") is None


def test_search_and_source_filter(store):
    store.add(item())
    store.add(item("mail", "email"))
    service = RetrievalService(store)
    assert len(service.search_context("machine learning")) == 2
    assert [result.source for result in service.search_emails("machine")] == ["email"]