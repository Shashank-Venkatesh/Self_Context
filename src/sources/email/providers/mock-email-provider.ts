import type { FetchEmailPageResult } from '../models/email-message.js';
import type { EmailProvider } from './email-provider.js';

export class MockEmailProvider implements EmailProvider {
  readonly name = 'mock';

  constructor(private readonly dataset: FetchEmailPageResult[] = []) {}

  async authenticate(): Promise<void> {}

  async fetchMessages(params: {
    cursor?: string | null;
    pageToken?: string;
    pageSize: number;
  }): Promise<FetchEmailPageResult> {
    const index = params.pageToken ? Number(params.pageToken) : 0;
    const page = this.dataset[index] ?? { messages: [] };
    if (!page.nextPageToken && this.dataset[index + 1]) {
      page.nextPageToken = String(index + 1);
    }
    return page;
  }
}
