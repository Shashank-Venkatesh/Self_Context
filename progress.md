# Project Progress

Last updated: 2026-09-29

## Project

Self Context is a Linux-first, local-first personal context library for AI. The current MVP pipeline is:

```text
Gmail API -> email provider -> normalization -> local SQLite/FTS5 -> retrieval -> MCP over stdio
```

The project is Python 3.11+, uses a `src/` layout, and exposes the `self-context` CLI.

## Current State

- XDG-aware configuration is implemented.
- Local SQLite storage, metadata, timestamps, CRUD/upsert, deletion, and FTS5 keyword search are implemented.
- Gmail OAuth uses the official Gmail API client and stores the token locally with mode `600`.
- Gmail pagination, MIME body decoding, HTML-to-text conversion, header decoding, domain filtering, and idempotent ingestion are implemented.
- A domain-filtered web source is implemented: `sync web` fetches pages over HTTP restricted to an explicit domain allowlist (exact domains and subdomains), normalizes them, and ingests them idempotently keyed by canonical URL.
- CLI commands are implemented for `init`, `config`, `auth gmail`, `sync email`, `sync web`, `search`, `get`, `status`, and `mcp`.
- MCP setup helpers are implemented: `mcp --print-config` prints the client configuration JSON, and `mcp --install claude|cline|cursor` merges the server entry into the chosen client's `mcpServers` config.
- MCP tools are implemented for `search_context`, `get_context_item`, `search_emails`, and `search_web`; the read-only `context://item/<id>` resource is also implemented.
- The repository contains automated tests for core storage/retrieval, email normalization/provider/ingestion behavior, CLI help, and MCP tool behavior.
- `TESTING.md` now documents automated checks, isolated CLI smoke tests, Gmail OAuth acceptance testing, synchronization/retrieval checks, MCP checks, privacy checks, and the regression workflow.
- `SETUP.md` now provides a simple first-run installation and usage guide for end users, including manual JSON client configuration and a one-click Cursor MCP deep-link setup.
- `PERSONAL_README.md` now provides a private, file-by-file architecture guide plus separate code-runtime and project-development workflows. It is intentionally ignored by Git.
- `PERSONAL_README.md` now places optional YouTube topic links beside the architecture topics they explain instead of using a separate links section.

## Work Completed

### Web source and MCP setup improvements

- Added a domain-filtered web scraping source under `src/self_context/sources/web/` with an HTTP provider restricted to an explicit domain allowlist (exact domains and subdomains), page normalization, and idempotent ingestion keyed by canonical URL.
- Added the `self-context sync web --url <url> --domain <domain> [--domain ...] [--timeout N]` CLI command; URLs outside the allowlist are skipped and reported.
- Added `self-context mcp --print-config` and `self-context mcp --install claude|cline|cursor`, which merges the server entry into the client's `mcpServers` configuration while preserving existing entries.
- Added the `search_web` MCP tool for searching locally indexed web page context.
- Updated `README.md`, `SETUP.md`, and `TESTING.md` to document the web source, the MCP setup commands, and the new tool.

### Documentation and testing guidance

- Added one-click Cursor MCP install deep-link configuration to `SETUP.md` to streamline client integration alongside Claude Desktop and Cline manual configs.
- Added `TESTING.md` with step-by-step instructions for setting up a development environment.
- Documented the commands for running pytest, coverage, and Ruff.
- Documented isolated CLI testing with temporary XDG directories.
- Documented Gmail OAuth setup, token permission checks, domain/query synchronization, search, and item retrieval.
- Documented MCP client configuration and verification of every exposed tool/resource.
- Documented error-path, privacy, filesystem, cleanup, and regression checks.

### Existing implementation baseline

- Generic `ContextItem` and normalized email models are present.
- Provider interfaces keep ingestion independent of Gmail-specific API details.
- Fake providers and services keep automated tests independent of credentials and network access.
- The CLI uses Click exceptions for user-facing failures and closes local stores after commands.

## Validation Status

Validation for the documentation change completed in this work session. The checks were:

```bash
.venv/bin/pytest -q
.venv/bin/pytest --cov=self_context --cov-report=term-missing
.venv/bin/ruff check src tests
```

Results: Documentation-only additions to `SETUP.md` and `progress.md`; `pytest -q` passed with 9 tests; Ruff completed with no violations.

The Gmail OAuth and MCP client flows require manual environment-specific acceptance testing as described in `TESTING.md`.

## Ongoing Maintenance Rule

Update this file whenever the codebase changes. Every entry must include:

- date
- files or area changed
- behavior or documentation impact
- focused validation and full validation results
- skipped checks, failures, or follow-up work

Do not mark a check as passing until it has actually been run. Keep the newest entry at the top of the log below.

## Progress Log

### 2026-09-29 (Web Source & MCP Setup)

- Files changed: `README.md`, `SETUP.md`, `TESTING.md`, `progress.md` (documentation only; implementation in `src/self_context/sources/web/`, `src/self_context/cli.py`, and `src/self_context/mcp/server.py` was completed separately).
- Behavior / documentation impact:
  - Documented the new domain-filtered web source: `sync web --url <url> --domain <domain>` with exact-domain and subdomain allowlist matching, skip reporting, and idempotent re-syncs keyed by canonical URL.
  - Documented `mcp --print-config` and `mcp --install claude|cline|cursor` alongside the existing manual JSON and Cursor deep-link instructions.
  - Documented the new `search_web` MCP tool and added web sync and MCP setup acceptance steps to `TESTING.md`.
- Focused and full validation: Documentation-only change; verified structure and tone against existing docs. Test suite and Ruff were not re-run because no code changed in this pass.
- Results: Documentation updated.
- Follow-up: Run the web sync and MCP install acceptance checks in `TESTING.md` against a live environment.

### 2026-09-28 (Feature Enhancements & Testing)

- Files changed: `src/self_context/config.py`, `src/self_context/cli.py`, `src/self_context/sources/email/providers.py`, `tests/test_cli.py`, `README.md`, `SETUP.md`, `progress.md`.
- Behavior / documentation impact:
  - Added user-selectable data directory storage via `--data-dir` on `init` and `config`, persisted in `config.json`.
  - Added interactive prompt asking for target scraping domain if `--domain` is not provided.
  - Added AI MCP connection link generation via `self-context link`, `self-context mcp-link`, and `self-context mcp --link` outputting Cursor deep links and MCP client JSON configurations.
  - Added `self-context update` command to easily refresh the context folder and keep it up to date.
  - Added interactive `self-context setup` wizard.
  - Added `get_profile` to `GmailProvider` to show authenticated user's email.
  - Expanded test suite with 6 new tests covering all CLI features.
- Focused and full validation:
  - Ran `ruff check src tests`: Passed (no violations).
  - Ran `pytest -v --cov=self_context`: 15 passed in 0.36s (78% total coverage).
- Results: All checks and tests passed.
- Follow-up: Ready for end-user testing and additional context source plugins.

### 2026-09-28

- Files changed: `SETUP.md`, `progress.md`.
- Behavior / documentation impact: Added user-friendly MCP setup documentation including the one-click Cursor deep link (`cursor://anysphere.cursor-deeplink/mcp/install?...`) and multi-client configuration guides (Claude Desktop, Cline, Cursor) to make integrating the local MCP server seamless.
- Focused and full validation: Verified formatting and structure against existing docs. Ran linter and test suite.
- Results: Documentation updated; tests and Ruff passing.
- Follow-up: Continue extending context sources and refining MCP tool signatures as needed.

### 2026-09-25

- Added optional YouTube reference links to the private personal guide for the main technologies used by the project.
- Reorganized the YouTube links into the relevant architecture sections so each reference appears beside the code it helps explain.
- Added private `PERSONAL_README.md` with personalized navigation instructions, repository architecture, command execution paths, test workflow, change workflow, and design rules.
- Added `PERSONAL_README.md` to `.gitignore` so the personal guide remains local.
- Added `SETUP.md` with concise setup steps for installation, initialization, optional Gmail access, email import, search, MCP configuration, checks, and troubleshooting.
- Added `TESTING.md` with the product testing workflow and acceptance checklist.
- Added this `progress.md` as the living project progress record.
- Validation: `.venv/bin/pytest -q` passed with 9 tests; `.venv/bin/ruff check src tests` passed with no violations. Coverage was not run separately because these changes only add documentation.
- Follow-up: keep this log synchronized with every future source, test, configuration, or documentation change.
