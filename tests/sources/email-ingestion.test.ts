import os from 'node:os';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { ContextStore } from '../../src/core/storage/context-store.js';
import { EmailIngestionService } from '../../src/sources/email/ingestion/email-ingestion-service.js';
import { MockEmailProvider } from '../../src/sources/email/providers/mock-email-provider.js';

function createStore(): ContextStore {
  return new ContextStore(path.join(os.tmpdir(), `self-context-${crypto.randomUUID()}.db`));
}

describe('EmailIngestionService', () => {
  it('normalizes and syncs paginated messages with dedupe tracking', async () => {
    const provider = new MockEmailProvider([
      {
        messages: [
          {
            id: 'm1',
            subject: 'Project Kickoff',
            from: 'lead@example.com',
            to: ['me@example.com'],
            body: 'Kickoff tomorrow',
            snippet: 'Kickoff',
            sentAt: '2026-01-01T00:00:00.000Z',
            updatedAt: '2026-01-01T00:00:00.000Z'
          }
        ],
        nextPageToken: '1',
        cursor: '100'
      },
      {
        messages: [
          {
            id: 'm1',
            subject: 'Project Kickoff',
            from: 'lead@example.com',
            to: ['me@example.com'],
            body: 'Kickoff tomorrow',
            snippet: 'Kickoff',
            sentAt: '2026-01-01T00:00:00.000Z',
            updatedAt: '2026-01-01T00:00:00.000Z'
          },
          {
            id: 'm2',
            subject: 'Follow up',
            from: 'pm@example.com',
            to: ['me@example.com'],
            body: 'Please review notes',
            snippet: 'review notes',
            sentAt: '2026-01-02T00:00:00.000Z',
            updatedAt: '2026-01-02T00:00:00.000Z'
          }
        ],
        cursor: '200'
      }
    ]);

    const store = createStore();
    const ingestion = new EmailIngestionService(provider, store, 50);

    const result = await ingestion.sync();

    expect(result.fetched).toBe(3);
    expect(result.insertedOrUpdated).toBe(3);
    expect(result.duplicatesSkipped).toBe(1);
    expect(result.cursor).toBe('200');
    expect(store.search('Kickoff', 10, 'email', 'mock')).toHaveLength(1);
    expect(store.search('review', 10, 'email', 'mock')).toHaveLength(1);

    store.close();
  });
});
