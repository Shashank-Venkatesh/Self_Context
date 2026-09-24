# Self Context

Self Context is a privacy-first local context library for AI systems. It ingests personal data sources (starting with email), normalizes and stores context locally, and exposes retrieval tools through an MCP server.

## Product Principles

- **Local first**: data remains on the user's machine by default.
- **AI agnostic**: works with any MCP-compatible client.
- **Source agnostic**: email is the first source, not the final architecture.
- **Privacy by design**: credentials and sensitive content are handled conservatively.

## MVP Architecture

```text
src/
├── core/
│   ├── models/       # ContextItem model
│   ├── storage/      # SQLite context store + sync state
│   └── retrieval/    # Retrieval abstraction
├── sources/
│   ├── base/         # Data source interfaces
│   └── email/
│       ├── providers/   # Email provider abstractions (Gmail + mock)
│       └── ingestion/   # Sync + normalization + deduplication
├── mcp/
│   ├── server/       # MCP server bootstrap
│   └── tools/        # Intent-oriented MCP tool handlers
└── main/             # Entry point
```

## Quick Start

### 1) Install

```bash
npm install
```

### 2) Configure environment

```bash
cp .env.example .env
```

Set Gmail OAuth values if using Gmail provider.

### 3) Build / test

```bash
npm run lint
npm run test
npm run build
```

### 4) Run MCP server locally

```bash
npm run dev
```

## Email Sync Flow

1. Configure Gmail OAuth credentials.
2. Call the `sync_email` MCP tool.
3. Self Context fetches Gmail messages through official Gmail APIs.
4. Messages are normalized to `ContextItem` records and stored in local SQLite.
5. Use `search_context` / `search_emails` to retrieve relevant context.

## MCP Tool Reference

- `search_context(query, limit?)`: search all local context.
- `search_emails(query, provider?, limit?)`: search email-only context.
- `get_context_item(id)`: fetch one record by id.
- `sync_email(provider?)`: run incremental email synchronization.

## Troubleshooting

- **Invalid environment configuration**: verify `.env` values and formats.
- **Gmail auth errors**: refresh token/client credentials may be missing or expired.
- **No search results**: run `sync_email` first to ingest data.

## Security Notes

See `/docs/security.md` for privacy and security practices.
