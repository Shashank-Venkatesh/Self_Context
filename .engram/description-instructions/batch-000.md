# Node Description Batch 1 of 4

Engram is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the prompt below and write
your JSON answer to the answer file.

## Prompt

You are documenting nodes in a knowledge graph.
For each entry below, write ONE concise factual plain-language sentence
describing what it is or does. Use only the provided context.
For a code symbol (kind=code-symbol — a function, class, or constant),
describe what the function/symbol does based on its name, source location
and neighbors — e.g. "Resolves the configured ontology profile from graphify.yaml.".
For an entity node (any other kind — e.g. a person, place, event, object),
describe what the entity is and its role, grounded in its type, its
relations (neighbors) and the provided citations/evidence — e.g.
"Lady Carfax, a wealthy heiress who disappears en route to Lausanne.".
Ground entity descriptions in the citations/evidence when present; do not
speculate beyond the context, so a node with no supporting context may be
left out of the reply.
LANGUAGE: each entry has a `lang=` marker giving the language of its source.
Write that entry's description in EXACTLY that language. Do not translate to
a single common language — match each node's source language individually.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "commit:repo:github.com/Shashank-Venkatesh/Self_Context@080e01abfdadc2cd9288900307a3d7e20e2499c3": "080e01a Foundational Layout has been set" | kind=Commit | source=git | neighbors=[Documentation, Foundation, 7b22d8e Foundational Documentation adde…, __init__.py, models.py, retrieval.py] | lang=pt
- "core_storage_contextstore": "ContextStore" | kind=code-symbol | source=src/self_context/core/storage.py:L13 | neighbors=[Retrieval service that keeps callers in…, RetrievalService, storage.py, ContextItem, .add(), .add_many()] | lang=en
- "self_context_cli": "cli.py" | kind=code-symbol | source=src/self_context/cli.py:L1 | neighbors=[080e01a Foundational Layout has been set, retrieval.py, storage.py, auth(), auth_gmail(), _config()] | lang=en
- "self_context_config_appconfig": "AppConfig" | kind=code-symbol | source=src/self_context/config.py:L15 | neighbors=[Native-style command line interface for…, Print one indexed context item as JSON., Show local index status., Start the local MCP server over stdio., Local-first personal context for AI., Create Self Context's local configurati…] | lang=en
- "email_providers_gmailprovider": "GmailProvider" | kind=code-symbol | source=src/self_context/sources/email/providers.py:L21 | neighbors=[Convert Gmail message payloads into rea…, _TextExtractor, providers.py, .authenticate(), .decode_body(), .fetch_messages()] | lang=en
- "tests_test_email": "test_email.py" | kind=code-symbol | source=tests/test_email.py:L1 | neighbors=[080e01a Foundational Layout has been set, encoded(), FakeGet, FakeMessages, FakeProvider, FakeService] | lang=en
- "email_ingestion_emailingestor": "EmailIngestor" | kind=code-symbol | source=src/self_context/sources/email/ingestion.py:L11 | neighbors=[ingestion.py, .__init__(), .sync(), EmailProvider, FakeGet, FakeMessages] | lang=en
- "self_context_cli_config": "_config()" | kind=code-symbol | source=src/self_context/cli.py:L17 | neighbors=[cli.py, auth_gmail(), get_item(), init(), mcp(), Show non-sensitive local paths and conf…] | lang=en
- "tests_test_email_fakemessages": "FakeMessages" | kind=code-symbol | source=tests/test_email.py:L55 | neighbors=[test_email.py, EmailIngestor, GmailProvider, .execute(), .get(), .__init__()] | lang=en
- "email_normalization_textextractor": "_TextExtractor" | kind=code-symbol | source=src/self_context/sources/email/normalization.py:L14 | neighbors=[normalization.py, readable_html(), NormalizedEmail, .handle_data(), .__init__(), .text()] | lang=en
- "email_providers_emailprovider": "EmailProvider" | kind=code-symbol | source=src/self_context/sources/email/providers.py:L14 | neighbors=[EmailIngestor, Email ingestion pipeline: fetch, normal…, providers.py, .authenticate(), .fetch_messages(), .get_message()] | lang=en
- "core_models": "models.py" | kind=code-symbol | source=src/self_context/core/models.py:L1 | neighbors=[080e01a Foundational Layout has been set, ContextItem, encode_metadata(), parse_datetime(), utc_now(), Source-independent context domain model…] | lang=en
- "core_retrieval_retrievalservice": "RetrievalService" | kind=code-symbol | source=src/self_context/core/retrieval.py:L7 | neighbors=[retrieval.py, ContextItem, .get_context_item(), .__init__(), .search_context(), .search_emails()] | lang=en
- "email_normalization": "normalization.py" | kind=code-symbol | source=src/self_context/sources/email/normalization.py:L1 | neighbors=[080e01a Foundational Layout has been set, _body(), decoded_header(), normalize_gmail_message(), readable_html(), _TextExtractor] | lang=en
- "email_providers": "providers.py" | kind=code-symbol | source=src/self_context/sources/email/providers.py:L1 | neighbors=[080e01a Foundational Layout has been set, build_domain_query(), EmailProvider, GmailProvider, parse_header(), parse_timestamp()] | lang=en
- "core_models_contextitem": "ContextItem" | kind=code-symbol | source=src/self_context/core/models.py:L16 | neighbors=[models.py, .to_dict(), Retrieval service that keeps callers in…, RetrievalService, ContextStore, SQLite-backed storage hidden behind a s…] | lang=en
- "core_storage": "storage.py" | kind=code-symbol | source=src/self_context/core/storage.py:L1 | neighbors=[080e01a Foundational Layout has been set, ContextStore, SQLite-backed storage hidden behind a s…, ingestion.py, server.py, cli.py] | lang=en
- "mcp_server": "server.py" | kind=code-symbol | source=src/self_context/mcp/server.py:L1 | neighbors=[080e01a Foundational Layout has been set, retrieval.py, storage.py, create_server(), run_server(), Local stdio MCP server exposing context…] | lang=en
- "self_context_cli_store": "_store()" | kind=code-symbol | source=src/self_context/cli.py:L23 | neighbors=[cli.py, get_item(), init(), search(), status(), sync_email()] | lang=en
- "tests_test_email_fakeget": "FakeGet" | kind=code-symbol | source=tests/test_email.py:L74 | neighbors=[test_email.py, EmailIngestor, GmailProvider, .execute(), .__init__(), .get()] | lang=en
- "tests_test_email_fakeprovider": "FakeProvider" | kind=code-symbol | source=tests/test_email.py:L36 | neighbors=[test_email.py, EmailIngestor, GmailProvider, .fetch_messages(), .__init__(), test_ingestion_handles_pagination_and_r…] | lang=en
- "tests_test_email_fakeservice": "FakeService" | kind=code-symbol | source=tests/test_email.py:L90 | neighbors=[test_email.py, EmailIngestor, GmailProvider, .__init__(), .users(), test_gmail_provider_uses_mocked_paginat…] | lang=en
- "tests_test_email_fakeusers": "FakeUsers" | kind=code-symbol | source=tests/test_email.py:L82 | neighbors=[test_email.py, .__init__(), EmailIngestor, GmailProvider, .__init__(), .messages()] | lang=en
- "branch:repo:github.com/Shashank-Venkatesh/Self_Context#Documentation": "Documentation" | kind=Branch | source=git | neighbors=[080e01a Foundational Layout has been set, 47aeaa5 Initial commit, 7b22d8e Foundational Documentation adde…, d1fd9cf Readme File update, e9af453 Add MIT License to the project] | lang=en
- "commit:repo:github.com/Shashank-Venkatesh/Self_Context@d1fd9cf6f6afa88a1ad853dffe0242fbd1602327": "d1fd9cf Readme File update" | kind=Commit | source=git | neighbors=[Documentation, Foundation, main, 080e01a Foundational Layout has been set, e9af453 Add MIT License to the project] | lang=en
- "commit:repo:github.com/Shashank-Venkatesh/Self_Context@e9af45330fd38959363e4728fdf89d5271db7c40": "e9af453 Add MIT License to the project" | kind=Commit | source=git | neighbors=[47aeaa5 Initial commit, Documentation, Foundation, main, d1fd9cf Readme File update] | lang=en
- "core_retrieval": "retrieval.py" | kind=code-symbol | source=src/self_context/core/retrieval.py:L1 | neighbors=[080e01a Foundational Layout has been set, RetrievalService, Retrieval service that keeps callers in…, server.py, cli.py] | lang=en
- "core_storage_contextstore_add": ".add()" | kind=code-symbol | source=src/self_context/core/storage.py:L42 | neighbors=[ContextStore, .get_by_source(), ._values(), .add_many(), .update()] | lang=en
- "email_ingestion": "ingestion.py" | kind=code-symbol | source=src/self_context/sources/email/ingestion.py:L1 | neighbors=[080e01a Foundational Layout has been set, models.py, storage.py, EmailIngestor, Email ingestion pipeline: fetch, normal…] | lang=en
- "self_context_cli_sync_email": "sync_email()" | kind=code-symbol | source=src/self_context/cli.py:L77 | neighbors=[cli.py, Fetch, normalize, and index Gmail messa…, _config(), _store(), sync()] | lang=en
- "branch:repo:github.com/Shashank-Venkatesh/Self_Context#Foundation": "Foundation" | kind=Branch | source=git | neighbors=[080e01a Foundational Layout has been set, 47aeaa5 Initial commit, d1fd9cf Readme File update, e9af453 Add MIT License to the project] | lang=en
- "commit:repo:github.com/Shashank-Venkatesh/Self_Context@47aeaa5e5ce5ca04b865da0c6f4e7ee5fd37af42": "47aeaa5 Initial commit" | kind=Commit | source=git | neighbors=[Documentation, Foundation, main, e9af453 Add MIT License to the project] | lang=en
- "core_storage_contextstore_from_row": "._from_row()" | kind=code-symbol | source=src/self_context/core/storage.py:L125 | neighbors=[ContextStore, .get(), .get_by_source(), .search()] | lang=en
- "email_normalization_readable_html": "readable_html()" | kind=code-symbol | source=src/self_context/sources/email/normalization.py:L26 | neighbors=[normalization.py, _body(), _TextExtractor, .text()] | lang=en
- "self_context_cli_get_item": "get_item()" | kind=code-symbol | source=src/self_context/cli.py:L110 | neighbors=[cli.py, _config(), _store(), Print one indexed context item as JSON.] | lang=en
- "self_context_cli_init": "init()" | kind=code-symbol | source=src/self_context/cli.py:L34 | neighbors=[cli.py, _config(), _store(), Create Self Context's local configurati…] | lang=en
- "self_context_cli_search": "search()" | kind=code-symbol | source=src/self_context/cli.py:L97 | neighbors=[cli.py, Search indexed context., _config(), _store()] | lang=en
- "self_context_cli_status": "status()" | kind=code-symbol | source=src/self_context/cli.py:L123 | neighbors=[cli.py, Show local index status., _config(), _store()] | lang=en
- "self_context_config": "config.py" | kind=code-symbol | source=src/self_context/config.py:L1 | neighbors=[080e01a Foundational Layout has been set, AppConfig, _xdg(), Filesystem and environment configuratio…] | lang=en
- "tests_test_core": "test_core.py" | kind=code-symbol | source=tests/test_core.py:L1 | neighbors=[080e01a Foundational Layout has been set, item(), test_search_and_source_filter(), test_store_crud_and_duplicate_upsert()] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /home/scatterzz/Documents/Projects/Self_Context/.engram/description-instructions/batch-000.json

Keep each description factual and concise (one sentence). No markdown, no prose
outside the JSON object. It is acceptable to omit a node if context is
insufficient — but include every node you can ground confidently.

Example answer format:
```json
{
  "node_id_1": "Resolves the configured ontology profile from graphify.yaml.",
  "node_id_2": "Colonel James Barclay, an antagonist in The Crooked Man."
}
```
