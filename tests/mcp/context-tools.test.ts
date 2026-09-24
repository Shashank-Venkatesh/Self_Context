import os from 'node:os';
import path from 'node:path';
import { describe, expect, it } from 'vitest';
import { createContextTools } from '../../src/mcp/tools/context-tools.js';
import { ContextRetriever } from '../../src/core/retrieval/context-retriever.js';
import { ContextStore } from '../../src/core/storage/context-store.js';
import { EmailIngestionService } from '../../src/sources/email/ingestion/email-ingestion-service.js';
import { MockEmailProvider } from '../../src/sources/email/providers/mock-email-provider.js';

function createStore(): ContextStore {
  return new ContextStore(path.join(os.tmpdir(), `self-context-${crypto.randomUUID()}.db`));
}

describe('context tools', () => {
  it('validates input and rejects unknown providers', async () => {
    const store = createStore();
    const retriever = new ContextRetriever(store);
    const tools = createContextTools({
      retriever,
      emailIngestionByProvider: {
        mock: new EmailIngestionService(new MockEmailProvider(), store, 20)
      }
    });

    await expect(tools.searchContext({ query: '' })).rejects.toThrow();
    await expect(tools.syncEmail({ provider: 'gmail' })).rejects.toThrow('Unsupported email provider');

    store.close();
  });
});
