import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import * as z from 'zod/v4';
import { createContextTools } from '../tools/context-tools.js';

export async function startMcpServer(params: Parameters<typeof createContextTools>[0]): Promise<void> {
  const tools = createContextTools(params);

  const server = new McpServer({
    name: 'self-context',
    version: '0.1.0'
  });

  server.registerTool(
    'search_context',
    {
      description:
        'Search user context across all local sources by keyword. Use this when you need personal context relevant to a topic.',
      inputSchema: {
        query: z.string().describe('Keyword query to search in locally indexed context'),
        limit: z.number().int().min(1).max(50).optional().describe('Maximum number of results (default: 20)')
      }
    },
    async ({ query, limit }) => {
      const results = await tools.searchContext({ query, limit });
      return {
        content: [{ type: 'text', text: JSON.stringify(results, null, 2) }]
      };
    }
  );

  server.registerTool(
    'search_emails',
    {
      description:
        'Search only indexed email context. Use this when the request is specifically about email messages or conversations.',
      inputSchema: {
        query: z.string().describe('Keyword query for email records'),
        provider: z.string().default('gmail').describe('Email provider identifier (default: gmail)'),
        limit: z.number().int().min(1).max(50).optional().describe('Maximum number of results (default: 20)')
      }
    },
    async ({ query, provider, limit }) => {
      const results = await tools.searchEmails({ query, provider, limit });
      return {
        content: [{ type: 'text', text: JSON.stringify(results, null, 2) }]
      };
    }
  );

  server.registerTool(
    'get_context_item',
    {
      description: 'Fetch one context item by id when a search result needs full detail.',
      inputSchema: {
        id: z.string().describe('Unique context item id')
      }
    },
    async ({ id }) => {
      const item = await tools.getContextItem({ id });
      return {
        content: [{ type: 'text', text: JSON.stringify(item, null, 2) }]
      };
    }
  );

  server.registerTool(
    'sync_email',
    {
      description:
        'Trigger local email synchronization for a provider. This ingests metadata/content into local storage without sending data to external AI APIs.',
      inputSchema: {
        provider: z.string().default('gmail').describe('Email provider identifier (default: gmail)')
      }
    },
    async ({ provider }) => {
      const sync = await tools.syncEmail({ provider });
      return {
        content: [{ type: 'text', text: JSON.stringify(sync, null, 2) }]
      };
    }
  );

  const transport = new StdioServerTransport();
  await server.connect(transport);
}
