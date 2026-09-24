export interface EmailMessage {
  id: string;
  threadId?: string;
  subject: string;
  from: string;
  to: string[];
  cc?: string[];
  snippet?: string;
  body: string;
  sentAt: string;
  updatedAt: string;
}

export interface FetchEmailPageResult {
  messages: EmailMessage[];
  nextPageToken?: string;
  cursor?: string;
}
