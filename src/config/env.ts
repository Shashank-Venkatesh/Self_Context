import path from 'node:path';
import { config as loadEnv } from 'dotenv';
import { z } from 'zod';

loadEnv();

const schema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  SELF_CONTEXT_DB_PATH: z.string().default(path.resolve(process.cwd(), 'data/self-context.db')),
  EMAIL_PROVIDER: z.enum(['mock', 'gmail']).default('mock'),
  EMAIL_SYNC_PAGE_SIZE: z.coerce.number().int().min(1).max(500).default(50),
  GOOGLE_OAUTH_CLIENT_ID: z.string().optional(),
  GOOGLE_OAUTH_CLIENT_SECRET: z.string().optional(),
  GOOGLE_OAUTH_REFRESH_TOKEN: z.string().optional(),
  GOOGLE_OAUTH_ACCESS_TOKEN: z.string().optional(),
  GOOGLE_EMAIL_ADDRESS: z.string().email().optional()
});

export type AppConfig = z.infer<typeof schema>;

export function getConfig(overrides: Partial<NodeJS.ProcessEnv> = {}): AppConfig {
  const parsed = schema.safeParse({ ...process.env, ...overrides });

  if (!parsed.success) {
    const message = parsed.error.issues.map((issue) => `${issue.path.join('.')}: ${issue.message}`).join('; ');
    throw new Error(`Invalid environment configuration: ${message}`);
  }

  return parsed.data;
}
