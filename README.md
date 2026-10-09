# Self Context

Self Context is a Linux-first, local-first personal context library for AI. The MVP imports Gmail email through the official API, normalizes it, stores it in a local SQLite database, and exposes local retrieval through an MCP server over stdio.

## Philosophy

- **Local-first:** context is stored under the user's XDG data directory.
- **Linux-first:** the CLI follows standard XDG paths and is the primary interface.
- **Privacy-focused:** there is no Self Context cloud backend, telemetry, or analytics.
- **CLI-driven:** initialization, authentication, sync, search, inspection, status, and MCP startup are terminal commands.
- **MCP-based:** compatible AI clients can request semantic context operations without accessing raw SQL or the database directly.

## Architecture

```text
Gmail API -> provider -> email ingestion -> normalization -> SQLite -> retrieval -> MCP -> AI client
```

The generic `ContextItem` model and `EmailProvider` protocol keep future sources separate from the core. Calendar, notes, files, GitHub, Slack, and browser history are not implemented in this MVP.

## Installation

Python 3.11 or newer is required.

```bash
python -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
```

For local development, the test and lint dependencies are included by the `dev` extra.

## CLI Usage

```bash
self-context init
self-context config
self-context auth gmail
self-context sync email --domain company.com
self-context sync email --domain company.com --domain partner.org
self-context search "project meeting"
self-context get email:<gmail-message-id>
self-context status
self-context mcp
```

`self-context sync email --domain company.com` restricts Gmail's API search to messages involving that domain in `From`, `To`, `Cc`, or `Bcc`. Repeat `--domain` for multiple approved domains and combine it with Gmail queries such as `--query 'newer_than:7d'`. Without `--domain`, the command preserves the normal Gmail query behavior. Search also supports `self-context search --source email` and `self-context search --type email`.

Commands return a non-zero exit code for configuration, authentication, storage, and source failures. Normal output does not include email bodies or credentials.

## Gmail Setup

1. Create a Google Cloud project and enable the Gmail API.
2. Create an OAuth client for a desktop application and download its JSON file.
3. Set the path before authentication:

```bash
export SELF_CONTEXT_GMAIL_CREDENTIALS=/absolute/path/to/client_secret.json
self-context auth gmail
```

The first authentication opens Google's official local OAuth flow. The refresh token is stored at the XDG configuration path with restrictive file permissions. Client secrets and tokens are never printed or logged. Domain filtering uses the official Gmail API search syntax; Self Context does not scrape the Gmail website or send email content to external services.

## Storage

Self Context uses SQLite with an FTS5 keyword index. By default:

- configuration and Gmail token: `~/.config/self-context/`
- database: `~/.local/share/self-context/context.sqlite3`
- cache: `~/.cache/self-context/`

`XDG_CONFIG_HOME`, `XDG_DATA_HOME`, and `XDG_CACHE_HOME` can override the base directories. `SELF_CONTEXT_GMAIL_CREDENTIALS` configures the OAuth client path.

## MCP Setup

`self-context mcp` starts a local stdio MCP server. Configure an MCP-compatible client to launch that command, for example:

```json
{
  "mcpServers": {
    "self-context": {
      "command": "/absolute/path/to/self-context",
      "args": ["mcp"]
    }
  }
}
```

The server exposes:

- `search_context(query, source?, type?)`
- `get_context_item(item_id)`
- `search_emails(query)`
- read-only resource `context://item/<id>`

It does not expose SQL, filesystem, database mutation, or public network transports.

## Privacy

Email contents remain in the local database after Gmail synchronization. Self Context does not upload the database, send context to an AI API, or run telemetry. An AI client receives data only when it requests it through the local MCP connection. Protect the Linux user account and local filesystem because the MVP does not encrypt the SQLite database at rest.

## Implemented

- XDG-aware configuration and local SQLite storage
- Generic `ContextItem` model with metadata and timestamps
- FTS5 keyword search with source and type filters
- Gmail OAuth using Google's official API client
- Gmail pagination, MIME normalization, HTML-to-text conversion, and idempotent ingestion
- Click CLI for init, config, auth, sync, search, get, status, and MCP
- Local stdio MCP tools and a read-only context resource
- Automated tests that mock providers and require no Gmail credentials

## Future

- Additional context sources
- Semantic search, embeddings, and vector retrieval
- Automatic or scheduled synchronization
- Richer context relationships
- Additional MCP resources
- Encryption at rest and more Linux integrations
- Packaging through distribution package managers or standalone binaries

## Development

```bash
.venv/bin/pytest -q
.venv/bin/ruff check src tests
```

Self Context is licensed under the MIT License. See [LICENSE](LICENSE).
