import type { ContextItem } from '../../core/models/context-item.js';
import type { SyncResult } from '../../sources/base/data-source.js';

export interface ContextToolSet {
  searchContext(input: { query: string; limit?: number }): Promise<ContextItem[]>;
  searchEmails(input: { query: string; limit?: number; provider?: string }): Promise<ContextItem[]>;
  getContextItem(input: { id: string }): Promise<ContextItem | null>;
  syncEmail(input: { provider?: string }): Promise<SyncResult>;
}
