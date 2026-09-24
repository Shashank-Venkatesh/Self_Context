import type { NewContextItem } from '../../../core/models/context-item.js';
import { ContextStore } from '../../../core/storage/context-store.js';
import type { DataSource, SyncResult } from '../../base/data-source.js';
import type { EmailMessage } from '../models/email-message.js';
import type { EmailProvider } from '../providers/email-provider.js';

export class EmailIngestionService implements DataSource {
  readonly source = 'email';
  readonly provider: string;

  constructor(
    private readonly emailProvider: EmailProvider,
    private readonly store: ContextStore,
    private readonly pageSize: number
  ) {
    this.provider = emailProvider.name;
  }

  get providerName(): string {
    return this.emailProvider.name;
  }

  get providerId(): string {
    return this.emailProvider.name;
  }

  async sync(): Promise<SyncResult> {
    const existingCursor = this.store.getSyncCursor(this.source, this.providerId);

    await this.emailProvider.authenticate();

    let fetched = 0;
    let insertedOrUpdated = 0;
    let duplicatesSkipped = 0;

    let pageToken: string | undefined;
    let cursor = existingCursor;

    do {
      const page = await this.emailProvider.fetchMessages({
        cursor: existingCursor,
        pageToken,
        pageSize: this.pageSize
      });

      fetched += page.messages.length;

      for (const message of page.messages) {
        const existing = this.store.getBySourceId(this.source, this.providerId, message.id);
        const normalized = this.normalizeMessage(message);
        this.store.upsert(normalized);
        insertedOrUpdated += 1;
        if (existing) {
          duplicatesSkipped += 1;
        }
      }

      if (page.cursor) {
        cursor = cursor ? String(Math.max(Number(cursor), Number(page.cursor))) : page.cursor;
      }

      pageToken = page.nextPageToken;
    } while (pageToken);

    this.store.setSyncCursor(this.source, this.providerId, cursor ?? null);

    return {
      fetched,
      insertedOrUpdated,
      duplicatesSkipped,
      cursor: cursor ?? null
    };
  }

  private normalizeMessage(message: EmailMessage): NewContextItem {
    return {
      source: 'email',
      provider: this.providerId,
      sourceId: message.id,
      type: 'email_message',
      title: message.subject || '(No subject)',
      content: `${message.snippet ?? ''}\n${message.body}`.trim(),
      metadata: {
        threadId: message.threadId,
        from: message.from,
        to: message.to,
        cc: message.cc ?? [],
        sentAt: message.sentAt
      },
      createdAt: message.sentAt,
      updatedAt: message.updatedAt
    };
  }
}
