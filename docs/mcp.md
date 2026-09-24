# MCP Usage

Self Context exposes context-oriented tools:

- `search_context(query, limit?)`
- `search_emails(query, provider?, limit?)`
- `get_context_item(id)`
- `sync_email(provider?)`

These tools are designed around user intent and avoid exposing storage internals.
