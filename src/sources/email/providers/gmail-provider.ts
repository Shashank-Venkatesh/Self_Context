import type { AppConfig } from '../../../config/env.js';
import type { FetchEmailPageResult } from '../models/email-message.js';
import type { EmailProvider } from './email-provider.js';

const GMAIL_API_BASE = 'https://gmail.googleapis.com/gmail/v1/users/me';
const OAUTH_TOKEN_URL = 'https://oauth2.googleapis.com/token';

interface GmailTokenResponse {
  access_token: string;
}

interface GmailListResponse {
  messages?: Array<{ id: string }>;
  nextPageToken?: string;
}

interface GmailMessageResponse {
  id: string;
  threadId: string;
  internalDate: string;
  snippet?: string;
  payload?: {
    headers?: Array<{ name: string; value: string }>;
    body?: { data?: string };
    parts?: Array<{ mimeType?: string; body?: { data?: string } }>;
  };
}

export class GmailProvider implements EmailProvider {
  readonly name = 'gmail';
  private accessToken: string | undefined;

  constructor(private readonly config: AppConfig) {
    this.accessToken = config.GOOGLE_OAUTH_ACCESS_TOKEN;
  }

  async authenticate(): Promise<void> {
    if (this.accessToken) {
      return;
    }

    const { GOOGLE_OAUTH_CLIENT_ID, GOOGLE_OAUTH_CLIENT_SECRET, GOOGLE_OAUTH_REFRESH_TOKEN } = this.config;
    if (!GOOGLE_OAUTH_CLIENT_ID || !GOOGLE_OAUTH_CLIENT_SECRET || !GOOGLE_OAUTH_REFRESH_TOKEN) {
      throw new Error('Gmail authentication is not configured. Set OAuth client id/secret + refresh token or an access token.');
    }

    const payload = new URLSearchParams({
      client_id: GOOGLE_OAUTH_CLIENT_ID,
      client_secret: GOOGLE_OAUTH_CLIENT_SECRET,
      refresh_token: GOOGLE_OAUTH_REFRESH_TOKEN,
      grant_type: 'refresh_token'
    });

    const response = await fetch(OAUTH_TOKEN_URL, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: payload
    });

    if (!response.ok) {
      throw new Error(`Gmail OAuth refresh failed (${response.status}).`);
    }

    const token = (await response.json()) as GmailTokenResponse;
    this.accessToken = token.access_token;
  }

  async fetchMessages(params: {
    cursor?: string | null;
    pageToken?: string;
    pageSize: number;
  }): Promise<FetchEmailPageResult> {
    await this.authenticate();

    const queryParams = new URLSearchParams({
      maxResults: String(params.pageSize)
    });

    if (params.pageToken) {
      queryParams.set('pageToken', params.pageToken);
    }

    if (params.cursor) {
      const timestamp = Math.floor(Number(params.cursor) / 1000);
      if (!Number.isNaN(timestamp) && timestamp > 0) {
        queryParams.set('q', `after:${timestamp}`);
      }
    }

    const listResponse = await this.fetchJson<GmailListResponse>(`${GMAIL_API_BASE}/messages?${queryParams.toString()}`);
    const messages = listResponse.messages ?? [];

    const normalized = await Promise.all(
      messages.map(async (message) => {
        const detail = await this.fetchJson<GmailMessageResponse>(
          `${GMAIL_API_BASE}/messages/${encodeURIComponent(message.id)}?format=full&metadataHeaders=From&metadataHeaders=To&metadataHeaders=Cc&metadataHeaders=Subject&metadataHeaders=Date`
        );

        const headerValue = (name: string): string => {
          return detail.payload?.headers?.find((header) => header.name.toLowerCase() === name.toLowerCase())?.value ?? '';
        };

        const textBody = this.extractBody(detail);
        const sentAt = new Date(Number(detail.internalDate)).toISOString();

        return {
          id: detail.id,
          threadId: detail.threadId,
          subject: headerValue('Subject') || '(No subject)',
          from: headerValue('From'),
          to: headerValue('To')
            .split(',')
            .map((recipient) => recipient.trim())
            .filter(Boolean),
          cc: headerValue('Cc')
            .split(',')
            .map((recipient) => recipient.trim())
            .filter(Boolean),
          snippet: detail.snippet,
          body: textBody,
          sentAt,
          updatedAt: sentAt
        };
      })
    );

    const newestCursor = normalized
      .map((message) => new Date(message.updatedAt).getTime())
      .sort((a, b) => b - a)[0];

    return {
      messages: normalized,
      nextPageToken: listResponse.nextPageToken,
      cursor: Number.isFinite(newestCursor) ? String(newestCursor) : params.cursor ?? undefined
    };
  }

  private async fetchJson<T>(url: string): Promise<T> {
    if (!this.accessToken) {
      throw new Error('Missing Gmail access token after authentication.');
    }

    const authHeader = 'Bearer ' + this.accessToken;
    const response = await fetch(url, {
      headers: {
        Authorization: authHeader
      }
    });

    if (response.status === 401) {
      this.accessToken = undefined;
      await this.authenticate();
      return this.fetchJson<T>(url);
    }

    if (!response.ok) {
      throw new Error(`Gmail API request failed (${response.status}).`);
    }

    return (await response.json()) as T;
  }

  private extractBody(message: GmailMessageResponse): string {
    const decode = (input: string): string => Buffer.from(input, 'base64url').toString('utf-8');
    const direct = message.payload?.body?.data;
    if (direct) {
      return decode(direct);
    }

    const textPart = message.payload?.parts?.find((part) => part.mimeType === 'text/plain' && part.body?.data)?.body?.data;
    if (textPart) {
      return decode(textPart);
    }

    return message.snippet ?? '';
  }
}
