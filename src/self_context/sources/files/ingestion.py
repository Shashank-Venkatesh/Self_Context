"""File ingestion pipeline: scan, normalize, map, and persist to ContextStore."""

from __future__ import annotations

from datetime import timezone

from ...core.models import ContextItem, utc_now
from ...core.storage import ContextStore
from .normalization import normalize_file_document
from .providers import LocalFileProvider


class FileIngestor:
    """Ingests scanned file documents into local ContextStore."""

    def __init__(self, provider: LocalFileProvider, store: ContextStore) -> None:
        self.provider = provider
        self.store = store

    def sync(self) -> int:
        """Scan, normalize, and save file documents into ContextStore."""
        count = 0
        now = utc_now()
        for file_doc in self.provider.scan_files():
            normalized = normalize_file_document(file_doc)
            source_id = normalized.relative_path or normalized.path
            item_id = f"file:{source_id}"

            mtime = normalized.mtime
            if mtime.tzinfo is None:
                mtime = mtime.replace(tzinfo=timezone.utc)

            item = ContextItem(
                id=item_id,
                source="file",
                source_id=source_id,
                type="file",
                title=normalized.title,
                content=normalized.content,
                metadata=normalized.metadata,
                created_at=mtime,
                updated_at=mtime,
                indexed_at=now,
            )
            self.store.add(item)
            count += 1

        return count
