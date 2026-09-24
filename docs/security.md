# Security and Privacy Model

Self Context is local-first by default:

- User data is stored in a local SQLite database.
- The MCP server runs locally over stdio.
- No hosted backend is required for the MVP.
- Email content is not logged to stdout/stderr by design.
- OAuth credentials are loaded from environment variables.

## Sensitive Data Handling

- Do not commit `.env` files.
- Keep OAuth secrets in environment configuration.
- Logs should only include operational counters (for example, processed counts), not raw email content.

## Future Hardening

The codebase cleanly separates configuration, storage, and retrieval so encryption-at-rest can be added without redesigning ingestion or MCP interfaces.
