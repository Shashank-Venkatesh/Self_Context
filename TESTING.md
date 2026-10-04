# Self Context Testing Guide

This guide covers automated verification, local CLI smoke tests, Gmail acceptance testing, MCP integration testing, failure paths, and privacy checks for the Self Context MVP.

## 1. Test prerequisites

Self Context requires Linux and Python 3.11 or newer.

From the repository root:

```bash
python3 --version
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
```

Confirm that the installed command points at this checkout:

```bash
.venv/bin/self-context --version
```

Use `.venv/bin/python`, `.venv/bin/pytest`, `.venv/bin/ruff`, and `.venv/bin/self-context` for the remaining commands so the test uses the project environment.

## 2. Run the automated test suite

Run the complete suite:

```bash
.venv/bin/pytest -q
```

The tests use `tmp_path` SQLite databases. They do not need Gmail credentials, a Google account, or network access. A passing run should report all tests passed with no failures or errors.

Run with coverage when changing implementation code:

```bash
.venv/bin/pytest --cov=self_context --cov-report=term-missing
```

For a focused change, run the closest test module first:

```bash
.venv/bin/pytest -q tests/test_core.py
.venv/bin/pytest -q tests/test_email.py
.venv/bin/pytest -q tests/test_mcp.py
.venv/bin/pytest -q tests/test_cli.py
```

Coverage currently exercises SQLite CRUD/upsert and FTS retrieval, email MIME normalization, provider pagination, domain-query validation, ingestion idempotency, and MCP tool functions. The real OAuth browser flow and most CLI commands require the manual checks below.

## 3. Run lint checks

```bash
.venv/bin/ruff check src tests
```

A successful command exits with status 0 and prints no violations. Run this after modifying Python files.

## 4. Isolated CLI smoke test

Use temporary XDG directories so the smoke test cannot alter the normal user profile:

```bash
export TEST_ROOT="$(mktemp -d)"
export XDG_CONFIG_HOME="$TEST_ROOT/config"
export XDG_DATA_HOME="$TEST_ROOT/data"
export XDG_CACHE_HOME="$TEST_ROOT/cache"
unset SELF_CONTEXT_GMAIL_CREDENTIALS
```

Initialize the local database:

```bash
.venv/bin/self-context init
.venv/bin/self-context status
.venv/bin/self-context config
```

Verify the following:

- `init` exits 0 and reports an initialized data directory.
- `status` exits 0, prints the database path under `$XDG_DATA_HOME/self-context`, and reports `items: 0`.
- `config` prints the three XDG-derived directories and `gmail_credentials: not configured`.
- The database file exists at `$XDG_DATA_HOME/self-context/context.sqlite3`.

Check empty retrieval and missing-item behavior:

```bash
.venv/bin/self-context search "anything"
.venv/bin/self-context get email:missing
printf 'search exit code: %s\n' "$?"
```

The search command should exit 0 with no result rows. The missing `get` command should exit non-zero and report `Context item not found: email:missing` without a traceback.

Check invalid domain validation:

```bash
.venv/bin/self-context sync email --domain 'not a domain'
printf 'sync exit code: %s\n' "$?"
```

It should exit non-zero and report an invalid email domain. No database item should be created.

## 5. Gmail OAuth acceptance test

Only run this section with a test account or an account approved for local development.

1. In Google Cloud, enable the Gmail API for a project.
2. Create a desktop OAuth client and download its client JSON file.
3. Set the path without placing the file in the repository:

```bash
export SELF_CONTEXT_GMAIL_CREDENTIALS="/absolute/path/to/client_secret.json"
```

4. Confirm configuration without printing the secret path contents:

```bash
.venv/bin/self-context config
```

The output should say `gmail_credentials: configured`; it should not print the client secret JSON or an email body.

5. Start authentication:

```bash
.venv/bin/self-context auth gmail
```

Complete Google's official browser flow. Verify that it exits 0 and prints `Gmail authentication completed.` Verify that the token is created at `$XDG_CONFIG_HOME/self-context/gmail-token.json` and has restrictive permissions:

```bash
stat -c '%a %n' "$XDG_CONFIG_HOME/self-context/gmail-token.json"
```

The expected mode is `600`. Never commit the client JSON or token.

## 6. Gmail synchronization and retrieval

Use a narrow query first to keep the test reproducible:

```bash
.venv/bin/self-context sync email --query 'newer_than:7d' --domain example.com
.venv/bin/self-context status
```

Verify that synchronization reports the number of messages and that `status` reports the same non-zero item count when matching mail exists. Repeat the exact sync command and verify that the count does not create duplicate database rows:

```bash
.venv/bin/self-context status
```

The ingestion path is keyed by Gmail message ID and should remain idempotent.

Search the imported data:

```bash
.venv/bin/self-context search "a word from a known subject or body"
.venv/bin/self-context search --source email "a known term"
.venv/bin/self-context search --type email "a known term"
```

Verify that matching rows show an `email:<gmail-message-id>` identifier and subject. Search should not print message bodies.

Retrieve one known result:

```bash
.venv/bin/self-context get email:<gmail-message-id>
```

Verify that the output is indented JSON containing the expected `id`, `source`, `source_id`, `type`, `title`, `content`, `metadata`, and timestamp fields. Confirm that the item content matches the source message and that no unrelated item is returned.

## 7. MCP acceptance test

Configure an MCP-compatible client to launch the installed command:

```json
{
  "mcpServers": {
    "self-context": {
      "command": "/absolute/path/to/repository/.venv/bin/self-context",
      "args": ["mcp"]
    }
  }
}
```

The client must launch the server over stdio, using the same XDG environment as the CLI. Verify that the server starts without writing non-protocol logs to stdout.

From the MCP client, exercise each exposed operation:

1. Call `search_context` with a known term. Confirm that matching context items are returned.
2. Call `search_context` with `source: "email"` and `type: "email"`. Confirm the filters are applied.
3. Call `search_emails` with a known term. Confirm that only email items are returned.
4. Call `get_context_item` with a known `email:<id>`. Confirm the item is returned.
5. Call `get_context_item` with an unknown ID. Confirm the result is `null`.
6. Read `context://item/<id>` for a known item. Confirm it returns the item representation.
7. Read `context://item/missing`. Confirm the client receives a not-found error.

Stop the client and verify that the CLI can still open the database afterward. The MCP server is read-only from its public interface and must not expose SQL or a public network listener.

## 8. Privacy and filesystem checks

Run these checks after an authenticated sync:

```bash
.venv/bin/self-context config
.venv/bin/self-context status
find "$XDG_CONFIG_HOME/self-context" "$XDG_DATA_HOME/self-context" -maxdepth 2 -type f -printf '%m %p\n'
```

Verify:

- No command output contains OAuth client JSON, refresh tokens, or full email bodies unless `get` or an MCP retrieval operation was explicitly requested.
- The OAuth token is mode `600`.
- The SQLite database remains under the configured local XDG data directory.
- No Self Context cloud endpoint, telemetry process, or unexpected network service is started.
- Credentials and test data are outside version control.

The MVP does not encrypt SQLite at rest. Treat the local database as sensitive and remove the temporary test directory when finished:

```bash
rm -rf "$TEST_ROOT"
unset TEST_ROOT XDG_CONFIG_HOME XDG_DATA_HOME XDG_CACHE_HOME SELF_CONTEXT_GMAIL_CREDENTIALS
```

## 9. Regression checklist for every code change

1. Update `progress.md` with the date, files changed, behavior changed, and validation performed.
2. Run the focused test module for the changed area.
3. Run `.venv/bin/pytest -q`.
4. Run `.venv/bin/ruff check src tests`.
5. Repeat the relevant CLI or MCP acceptance check when the change affects a user-facing command or protocol surface.
6. Record failures, skipped checks, and known follow-up work in `progress.md`.
