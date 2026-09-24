import { getConfig } from '../config/env.js';
import { ContextRetriever } from '../core/retrieval/context-retriever.js';
import { ContextStore } from '../core/storage/context-store.js';
import { startMcpServer } from '../mcp/server/create-server.js';
import { EmailIngestionService } from '../sources/email/ingestion/email-ingestion-service.js';
import { GmailProvider } from '../sources/email/providers/gmail-provider.js';
import { MockEmailProvider } from '../sources/email/providers/mock-email-provider.js';

async function main(): Promise<void> {
  const config = getConfig();
  const store = new ContextStore(config.SELF_CONTEXT_DB_PATH);
  const retriever = new ContextRetriever(store);

  const providers = {
    gmail: new GmailProvider(config),
    mock: new MockEmailProvider()
  };

  const emailIngestionByProvider = Object.fromEntries(
    Object.entries(providers).map(([name, provider]) => [name, new EmailIngestionService(provider, store, config.EMAIL_SYNC_PAGE_SIZE)])
  );

  await startMcpServer({
    retriever,
    emailIngestionByProvider
  });
}

main().catch((error) => {
  const message = error instanceof Error ? error.message : 'Unknown startup error';
  console.error(`Self Context failed to start: ${message}`);
  process.exit(1);
});
