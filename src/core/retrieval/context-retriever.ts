import type { ContextItem } from '../models/context-item.js';
import { ContextStore } from '../storage/context-store.js';

export class ContextRetriever {
  constructor(private readonly store: ContextStore) {}

  searchContext(query: string, limit = 20): ContextItem[] {
    return this.store.search(query, limit);
  }

  searchEmails(query: string, limit = 20, provider = 'gmail'): ContextItem[] {
    return this.store.search(query, limit, 'email', provider);
  }

  getContextItem(id: string): ContextItem | null {
    return this.store.getById(id);
  }
}
