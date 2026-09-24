export type ContextSource = 'email';

export interface ContextItem {
  id: string;
  source: ContextSource;
  provider: string;
  sourceId: string;
  type: string;
  title: string;
  content: string;
  metadata: Record<string, unknown>;
  createdAt: string;
  updatedAt: string;
  indexedAt: string;
}

export interface NewContextItem {
  source: ContextSource;
  provider: string;
  sourceId: string;
  type: string;
  title: string;
  content: string;
  metadata: Record<string, unknown>;
  createdAt: string;
  updatedAt: string;
}
