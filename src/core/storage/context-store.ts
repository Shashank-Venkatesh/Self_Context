import fs from 'node:fs';
import path from 'node:path';
import { randomUUID } from 'node:crypto';
import Database from 'better-sqlite3';
import type { ContextItem, NewContextItem } from '../models/context-item.js';

interface ContextRow {
  id: string;
  source: string;
  provider: string;
  source_id: string;
  type: string;
  title: string;
  content: string;
  metadata: string;
  created_at: string;
  updated_at: string;
  indexed_at: string;
}

export class ContextStore {
  private readonly db: Database.Database;

  constructor(dbPath: string) {
    fs.mkdirSync(path.dirname(dbPath), { recursive: true });
    this.db = new Database(dbPath);
    this.db.pragma('journal_mode = WAL');
    this.initialize();
  }

  private initialize(): void {
    this.db.exec(`
      CREATE TABLE IF NOT EXISTS context_items (
        id TEXT PRIMARY KEY,
        source TEXT NOT NULL,
        provider TEXT NOT NULL,
        source_id TEXT NOT NULL,
        type TEXT NOT NULL,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        metadata TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        indexed_at TEXT NOT NULL,
        UNIQUE(source, provider, source_id)
      );

      CREATE VIRTUAL TABLE IF NOT EXISTS context_items_fts USING fts5(
        id UNINDEXED,
        title,
        content,
        source,
        provider,
        type
      );

      CREATE TABLE IF NOT EXISTS sync_state (
        source TEXT NOT NULL,
        provider TEXT NOT NULL,
        cursor TEXT,
        updated_at TEXT NOT NULL,
        PRIMARY KEY(source, provider)
      );

      CREATE INDEX IF NOT EXISTS idx_context_source ON context_items(source, provider);
      CREATE INDEX IF NOT EXISTS idx_context_updated ON context_items(updated_at);
    `);
  }

  close(): void {
    this.db.close();
  }

  upsert(item: NewContextItem): ContextItem {
    const now = new Date().toISOString();
    const existing = this.db
      .prepare('SELECT id FROM context_items WHERE source = ? AND provider = ? AND source_id = ?')
      .get(item.source, item.provider, item.sourceId) as { id: string } | undefined;

    const id = existing?.id ?? randomUUID();

    const tx = this.db.transaction(() => {
      this.db
        .prepare(
          `INSERT INTO context_items (
            id, source, provider, source_id, type, title, content, metadata, created_at, updated_at, indexed_at
          ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
          ON CONFLICT(source, provider, source_id) DO UPDATE SET
            title = excluded.title,
            content = excluded.content,
            metadata = excluded.metadata,
            created_at = excluded.created_at,
            updated_at = excluded.updated_at,
            indexed_at = excluded.indexed_at`
        )
        .run(
          id,
          item.source,
          item.provider,
          item.sourceId,
          item.type,
          item.title,
          item.content,
          JSON.stringify(item.metadata),
          item.createdAt,
          item.updatedAt,
          now
        );

      this.db.prepare('DELETE FROM context_items_fts WHERE id = ?').run(id);
      this.db
        .prepare(
          'INSERT INTO context_items_fts (id, title, content, source, provider, type) VALUES (?, ?, ?, ?, ?, ?)'
        )
        .run(id, item.title, item.content, item.source, item.provider, item.type);
    });

    tx();

    return this.getById(id)!;
  }

  getById(id: string): ContextItem | null {
    const row = this.db.prepare('SELECT * FROM context_items WHERE id = ?').get(id) as ContextRow | undefined;
    return row ? this.mapRow(row) : null;
  }

  getBySourceId(source: string, provider: string, sourceId: string): ContextItem | null {
    const row = this.db
      .prepare('SELECT * FROM context_items WHERE source = ? AND provider = ? AND source_id = ?')
      .get(source, provider, sourceId) as ContextRow | undefined;
    return row ? this.mapRow(row) : null;
  }

  search(query: string, limit = 20, source?: string, provider?: string): ContextItem[] {
    if (!query.trim()) {
      return [];
    }

    const terms = query
      .trim()
      .split(/\s+/)
      .map((term) => term.replace(/[^\p{L}\p{N}_]/gu, ''))
      .filter(Boolean);

    if (terms.length === 0) {
      return [];
    }

    const match = terms.map((term) => `${term}*`).join(' AND ');

    const where: string[] = ['context_items_fts MATCH ?'];
    const args: unknown[] = [match];

    if (source) {
      where.push('ci.source = ?');
      args.push(source);
    }

    if (provider) {
      where.push('ci.provider = ?');
      args.push(provider);
    }

    args.push(limit);

    const rows = this.db
      .prepare(
        `SELECT ci.*
         FROM context_items_fts
         JOIN context_items ci ON ci.id = context_items_fts.id
         WHERE ${where.join(' AND ')}
         ORDER BY bm25(context_items_fts)
         LIMIT ?`
      )
      .all(...args) as ContextRow[];

    return rows.map((row) => this.mapRow(row));
  }

  getSyncCursor(source: string, provider: string): string | null {
    const row = this.db
      .prepare('SELECT cursor FROM sync_state WHERE source = ? AND provider = ?')
      .get(source, provider) as { cursor: string | null } | undefined;
    return row?.cursor ?? null;
  }

  setSyncCursor(source: string, provider: string, cursor: string | null): void {
    this.db
      .prepare(
        `INSERT INTO sync_state (source, provider, cursor, updated_at)
         VALUES (?, ?, ?, ?)
         ON CONFLICT(source, provider) DO UPDATE SET
          cursor = excluded.cursor,
          updated_at = excluded.updated_at`
      )
      .run(source, provider, cursor, new Date().toISOString());
  }

  private mapRow(row: ContextRow): ContextItem {
    return {
      id: row.id,
      source: row.source as ContextItem['source'],
      provider: row.provider,
      sourceId: row.source_id,
      type: row.type,
      title: row.title,
      content: row.content,
      metadata: JSON.parse(row.metadata),
      createdAt: row.created_at,
      updatedAt: row.updated_at,
      indexedAt: row.indexed_at
    };
  }
}
