# Project Progress

Last updated: 2026-09-25

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
- CLI commands are implemented for `init`, `config`, `auth gmail`, `sync email`, `search`, `get`, `status`, and `mcp`.
- MCP tools are implemented for `search_context`, `get_context_item`, and `search_emails`; the read-only `context://item/<id>` resource is also implemented.
- The repository contains automated tests for core storage/retrieval, email normalization/provider/ingestion behavior, CLI help, and MCP tool behavior.
- `TESTING.md` now documents automated checks, isolated CLI smoke tests, Gmail OAuth acceptance testing, synchronization/retrieval checks, MCP checks, privacy checks, and the regression workflow.
- `SETUP.md` now provides a simple first-run installation and usage guide for end users.
- `PERSONAL_README.md` now provides a private, file-by-file architecture guide plus separate code-runtime and project-development workflows. It is intentionally ignored by Git.
- `PERSONAL_README.md` now places optional YouTube topic links beside the architecture topics they explain instead of using a separate links section.

## Work Completed

### Documentation and testing guidance

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

Results: `pytest -q` passed with 9 tests; Ruff completed with no violations. Coverage was not run separately because this documentation-only change does not alter executable code.

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
