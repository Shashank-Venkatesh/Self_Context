import type { FetchEmailPageResult } from '../models/email-message.js';

export interface EmailProvider {
  readonly name: string;
  authenticate(): Promise<void>;
  fetchMessages(params: { cursor?: string | null; pageToken?: string; pageSize: number }): Promise<FetchEmailPageResult>;
}
