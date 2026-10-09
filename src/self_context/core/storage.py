"""SQLite-backed storage hidden behind a small context store API."""

from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Iterable

from .models import ContextItem, encode_metadata, parse_datetime


class ContextStore:
    def __init__(self, database_path: str | Path):
        self.database_path = str(database_path)
        if self.database_path != ":memory:":
            Path(self.database_path).parent.mkdir(parents=True, exist_ok=True)
        self._connection = sqlite3.connect(self.database_path)
        self._connection.row_factory = sqlite3.Row
        self._connection.execute("PRAGMA foreign_keys = ON")
        self._initialize()

    def _initialize(self) -> None:
        self._connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS context_items (
                id TEXT PRIMARY KEY, source TEXT NOT NULL, source_id TEXT NOT NULL,
                type TEXT NOT NULL, title TEXT NOT NULL, content TEXT NOT NULL,
                metadata TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
                indexed_at TEXT NOT NULL, UNIQUE(source, source_id)
            );
            CREATE VIRTUAL TABLE IF NOT EXISTS context_items_fts USING fts5(
                id UNINDEXED, title, content, metadata
            );
            """
        )
        self._connection.commit()

    def close(self) -> None:
        self._connection.close()

    def add(self, item: ContextItem) -> ContextItem:
        self._connection.execute(
            """INSERT INTO context_items
            (id, source, source_id, type, title, content, metadata, created_at,
             updated_at, indexed_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source, source_id) DO UPDATE SET
              title=excluded.title, content=excluded.content, metadata=excluded.metadata,
              updated_at=excluded.updated_at, indexed_at=excluded.indexed_at""",
            self._values(item),
        )
        self._connection.execute("DELETE FROM context_items_fts WHERE id = ?", (item.id,))
        self._connection.execute(
            "INSERT INTO context_items_fts VALUES (?, ?, ?, ?)",
            (item.id, item.title, item.content, encode_metadata(item.metadata)),
        )
        self._connection.commit()
        return self.get_by_source(item.source, item.source_id) or item

    def add_many(self, items: Iterable[ContextItem]) -> int:
        count = 0
        for item in items:
            self.add(item)
            count += 1
        return count

    def get(self, item_id: str) -> ContextItem | None:
        row = self._connection.execute(
            "SELECT * FROM context_items WHERE id = ?", (item_id,)
        ).fetchone()
        return self._from_row(row) if row else None

    def get_by_source(self, source: str, source_id: str) -> ContextItem | None:
        row = self._connection.execute(
            "SELECT * FROM context_items WHERE source = ? AND source_id = ?", (source, source_id)
        ).fetchone()
        return self._from_row(row) if row else None

    def update(self, item: ContextItem) -> ContextItem:
        if not self.get(item.id):
            raise KeyError(item.id)
        return self.add(item)

    def delete(self, item_id: str) -> bool:
        cursor = self._connection.execute("DELETE FROM context_items WHERE id = ?", (item_id,))
        self._connection.execute("DELETE FROM context_items_fts WHERE id = ?", (item_id,))
        self._connection.commit()
        return cursor.rowcount > 0

    def search(self, query: str, source: str | None = None, type: str | None = None,
               limit: int = 20) -> list[ContextItem]:
        terms = " ".join(part for part in query.split() if part)
        if not terms:
            return []
        clauses = ["context_items_fts MATCH ?"]
        params: list[object] = [terms]
        if source:
            clauses.append("items.source = ?")
            params.append(source)
        if type:
            clauses.append("items.type = ?")
            params.append(type)
        params.append(limit)
        query_sql = (
            "SELECT items.* FROM context_items_fts "
            "JOIN context_items items ON items.id = context_items_fts.id "
            f"WHERE {' AND '.join(clauses)} ORDER BY items.updated_at DESC LIMIT ?"
        )
        rows = self._connection.execute(query_sql, params).fetchall()
        return [self._from_row(row) for row in rows]

    def count(self) -> int:
        return int(self._connection.execute("SELECT COUNT(*) FROM context_items").fetchone()[0])

    @staticmethod
    def _values(item: ContextItem) -> tuple[object, ...]:
        return (
            item.id, item.source, item.source_id, item.type, item.title, item.content,
            encode_metadata(item.metadata), item.created_at.isoformat(),
            item.updated_at.isoformat(), item.indexed_at.isoformat(),
        )

    @staticmethod
    def _from_row(row: sqlite3.Row) -> ContextItem:
        return ContextItem(row["id"], row["source"], row["source_id"], row["type"], row["title"],
                           row["content"], json.loads(row["metadata"]),
                           parse_datetime(row["created_at"]), parse_datetime(row["updated_at"]),
                           parse_datetime(row["indexed_at"]))