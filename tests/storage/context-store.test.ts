import os from 'node:os';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { ContextStore } from '../../src/core/storage/context-store.js';

function createStore(): ContextStore {
  return new ContextStore(path.join(os.tmpdir(), `self-context-${crypto.randomUUID()}.db`));
}

describe('ContextStore', () => {
  it('upserts without creating duplicate records for same source id', () => {
    const store = createStore();

    const first = store.upsert({
      source: 'email',
      provider: 'gmail',
      sourceId: 'msg-1',
      type: 'email_message',
      title: 'Subject A',
      content: 'hello world',
      metadata: { from: 'a@example.com' },
      createdAt: '2026-01-01T00:00:00.000Z',
      updatedAt: '2026-01-01T00:00:00.000Z'
    });

    const second = store.upsert({
      source: 'email',
      provider: 'gmail',
      sourceId: 'msg-1',
      type: 'email_message',
      title: 'Subject A updated',
      content: 'hello world updated',
      metadata: { from: 'a@example.com' },
      createdAt: '2026-01-01T00:00:00.000Z',
      updatedAt: '2026-01-02T00:00:00.000Z'
    });

    const results = store.search('updated', 10);

    expect(second.id).toBe(first.id);
    expect(results).toHaveLength(1);
    expect(results[0]?.title).toBe('Subject A updated');

    store.close();
  });

  it('stores and retrieves sync cursor', () => {
    const store = createStore();

    store.setSyncCursor('email', 'gmail', '12345');

    expect(store.getSyncCursor('email', 'gmail')).toBe('12345');
    store.close();
  });
});
