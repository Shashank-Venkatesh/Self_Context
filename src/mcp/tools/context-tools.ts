import { z } from 'zod';
import { ContextRetriever } from '../../core/retrieval/context-retriever.js';
import type { SyncResult } from '../../sources/base/data-source.js';
import { EmailIngestionService } from '../../sources/email/ingestion/email-ingestion-service.js';
import type { ContextToolSet } from './tool-types.js';

const searchSchema = z.object({
  query: z.string().min(1),
  limit: z.number().int().min(1).max(50).optional()
});

const searchEmailSchema = searchSchema.extend({
  provider: z.string().default('gmail')
});

const getByIdSchema = z.object({
  id: z.string().min(1)
});

const syncSchema = z.object({
  provider: z.string().default('gmail')
});

export function createContextTools(params: {
  retriever: ContextRetriever;
  emailIngestionByProvider: Record<string, EmailIngestionService>;
}): ContextToolSet {
  const { retriever, emailIngestionByProvider } = params;

  return {
    async searchContext(input) {
      const { query, limit = 20 } = searchSchema.parse(input);
      return retriever.searchContext(query, limit);
    },

    async searchEmails(input) {
      const { query, limit = 20, provider } = searchEmailSchema.parse(input);
      return retriever.searchEmails(query, limit, provider);
    },

    async getContextItem(input) {
      const { id } = getByIdSchema.parse(input);
      return retriever.getContextItem(id);
    },

    async syncEmail(input): Promise<SyncResult> {
      const { provider } = syncSchema.parse(input ?? {});
      const ingestion = emailIngestionByProvider[provider];
      if (!ingestion) {
        throw new Error(`Unsupported email provider: ${provider}`);
      }
      return ingestion.sync();
    }
  };
}
