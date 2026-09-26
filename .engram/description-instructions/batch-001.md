# Node Description Batch 2 of 4

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

- "tests_test_email_test_ingestion_handles_pagination_and_repeat_sync": "test_ingestion_handles_pagination_and_repeat_sync()" | kind=code-symbol | source=tests/test_email.py:L45 | neighbors=[test_email.py, encoded(), FakeProvider, message()] | lang=en
- "branch:repo:github.com/Shashank-Venkatesh/Self_Context#main": "main" | kind=Branch | source=git | neighbors=[47aeaa5 Initial commit, d1fd9cf Readme File update, e9af453 Add MIT License to the project] | lang=en
- "core_retrieval_rationale_1": "Retrieval service that keeps callers independent of the storage engine." | kind=entity | source=src/self_context/core/retrieval.py:L1 | neighbors=[ContextItem, retrieval.py, ContextStore] | lang=en
- "core_storage_contextstore_get": ".get()" | kind=code-symbol | source=src/self_context/core/storage.py:L68 | neighbors=[ContextStore, ._from_row(), .update()] | lang=en
- "core_storage_contextstore_get_by_source": ".get_by_source()" | kind=code-symbol | source=src/self_context/core/storage.py:L74 | neighbors=[ContextStore, .add(), ._from_row()] | lang=en
- "core_storage_contextstore_update": ".update()" | kind=code-symbol | source=src/self_context/core/storage.py:L80 | neighbors=[ContextStore, .add(), .get()] | lang=en
- "email_models": "models.py" | kind=code-symbol | source=src/self_context/sources/email/models.py:L1 | neighbors=[080e01a Foundational Layout has been set, NormalizedEmail, Normalized email model independent of a…] | lang=en
- "email_models_normalizedemail": "NormalizedEmail" | kind=code-symbol | source=src/self_context/sources/email/models.py:L8 | neighbors=[models.py, Convert Gmail message payloads into rea…, _TextExtractor] | lang=en
- "email_normalization_body": "_body()" | kind=code-symbol | source=src/self_context/sources/email/normalization.py:L39 | neighbors=[normalization.py, readable_html(), normalize_gmail_message()] | lang=en
- "email_normalization_normalize_gmail_message": "normalize_gmail_message()" | kind=code-symbol | source=src/self_context/sources/email/normalization.py:L63 | neighbors=[normalization.py, _body(), decoded_header()] | lang=en
- "email_normalization_rationale_1": "Convert Gmail message payloads into readable normalized email records." | kind=entity | source=src/self_context/sources/email/normalization.py:L1 | neighbors=[NormalizedEmail, normalization.py, GmailProvider] | lang=en
- "self_context_cli_auth_gmail": "auth_gmail()" | kind=code-symbol | source=src/self_context/cli.py:L59 | neighbors=[cli.py, _config(), Complete the official Gmail OAuth flow …] | lang=en
- "self_context_cli_mcp": "mcp()" | kind=code-symbol | source=src/self_context/cli.py:L136 | neighbors=[cli.py, _config(), Start the local MCP server over stdio.] | lang=en
- "self_context_cli_sync": "sync()" | kind=code-symbol | source=src/self_context/cli.py:L70 | neighbors=[cli.py, Synchronize configured sources into loc…, sync_email()] | lang=en
- "tests_test_cli": "test_cli.py" | kind=code-symbol | source=tests/test_cli.py:L1 | neighbors=[080e01a Foundational Layout has been set, cli.py, test_sync_email_help_describes_domain_f…] | lang=en
- "tests_test_core_item": "item()" | kind=code-symbol | source=tests/test_core.py:L7 | neighbors=[test_core.py, test_search_and_source_filter(), test_store_crud_and_duplicate_upsert()] | lang=en
- "tests_test_email_encoded": "encoded()" | kind=code-symbol | source=tests/test_email.py:L9 | neighbors=[test_email.py, test_ingestion_handles_pagination_and_r…, test_normalizes_plain_html_and_multipar…] | lang=en
- "tests_test_email_message": "message()" | kind=code-symbol | source=tests/test_email.py:L13 | neighbors=[test_email.py, test_ingestion_handles_pagination_and_r…, test_normalizes_plain_html_and_multipar…] | lang=en
- "tests_test_email_test_gmail_provider_uses_mocked_paginated_api": "test_gmail_provider_uses_mocked_paginated_api()" | kind=code-symbol | source=tests/test_email.py:L98 | neighbors=[test_email.py, .fetch_messages(), FakeService] | lang=en
- "tests_test_email_test_normalizes_plain_html_and_multipart": "test_normalizes_plain_html_and_multipart()" | kind=code-symbol | source=tests/test_email.py:L23 | neighbors=[test_email.py, encoded(), message()] | lang=en
- "commit:repo:github.com/Shashank-Venkatesh/Self_Context@7b22d8e3049797cbbfc532e25d9f8f76faa8771e": "7b22d8e Foundational Documentation added to the code base" | kind=Commit | source=git | neighbors=[080e01a Foundational Layout has been set, Documentation] | lang=en
- "core_init": "__init__.py" | kind=code-symbol | source=src/self_context/core/__init__.py:L1 | neighbors=[080e01a Foundational Layout has been set, Core domain, storage, and retrieval ser…] | lang=en
- "core_retrieval_retrievalservice_search_context": ".search_context()" | kind=code-symbol | source=src/self_context/core/retrieval.py:L11 | neighbors=[RetrievalService, .search_emails()] | lang=en
- "core_retrieval_retrievalservice_search_emails": ".search_emails()" | kind=code-symbol | source=src/self_context/core/retrieval.py:L18 | neighbors=[RetrievalService, .search_context()] | lang=en
- "core_storage_contextstore_add_many": ".add_many()" | kind=code-symbol | source=src/self_context/core/storage.py:L61 | neighbors=[ContextStore, .add()] | lang=en
- "core_storage_contextstore_init": ".__init__()" | kind=code-symbol | source=src/self_context/core/storage.py:L14 | neighbors=[ContextStore, ._initialize()] | lang=en
- "core_storage_contextstore_initialize": "._initialize()" | kind=code-symbol | source=src/self_context/core/storage.py:L23 | neighbors=[ContextStore, .__init__()] | lang=en
- "core_storage_contextstore_search": ".search()" | kind=code-symbol | source=src/self_context/core/storage.py:L91 | neighbors=[ContextStore, ._from_row()] | lang=en
- "core_storage_contextstore_values": "._values()" | kind=code-symbol | source=src/self_context/core/storage.py:L117 | neighbors=[ContextStore, .add()] | lang=en
- "core_storage_rationale_1": "SQLite-backed storage hidden behind a small context store API." | kind=entity | source=src/self_context/core/storage.py:L1 | neighbors=[ContextItem, storage.py] | lang=pt
- "email_ingestion_rationale_1": "Email ingestion pipeline: fetch, normalize, map, and idempotently persist." | kind=entity | source=src/self_context/sources/email/ingestion.py:L1 | neighbors=[ingestion.py, EmailProvider] | lang=en
- "email_init": "__init__.py" | kind=code-symbol | source=src/self_context/sources/email/__init__.py:L1 | neighbors=[080e01a Foundational Layout has been set, Email source integration.] | lang=en
- "email_normalization_decoded_header": "decoded_header()" | kind=code-symbol | source=src/self_context/sources/email/normalization.py:L32 | neighbors=[normalization.py, normalize_gmail_message()] | lang=en
- "email_normalization_textextractor_text": ".text()" | kind=code-symbol | source=src/self_context/sources/email/normalization.py:L22 | neighbors=[readable_html(), _TextExtractor] | lang=en
- "email_providers_build_domain_query": "build_domain_query()" | kind=code-symbol | source=src/self_context/sources/email/providers.py:L89 | neighbors=[providers.py, Build a Gmail search query restricted t…] | lang=en
- "mcp_init": "__init__.py" | kind=code-symbol | source=src/self_context/mcp/__init__.py:L1 | neighbors=[080e01a Foundational Layout has been set, Model Context Protocol integration.] | lang=en
- "mcp_server_create_server": "create_server()" | kind=code-symbol | source=src/self_context/mcp/server.py:L14 | neighbors=[server.py, run_server()] | lang=en
- "mcp_server_run_server": "run_server()" | kind=code-symbol | source=src/self_context/mcp/server.py:L44 | neighbors=[server.py, create_server()] | lang=en
- "self_context_cli_auth": "auth()" | kind=code-symbol | source=src/self_context/cli.py:L54 | neighbors=[cli.py, Authenticate an external source.] | lang=en
- "self_context_cli_main": "main()" | kind=code-symbol | source=src/self_context/cli.py:L29 | neighbors=[cli.py, Local-first personal context for AI.] | lang=en

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /home/scatterzz/Documents/Projects/Self_Context/.engram/description-instructions/batch-001.json

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
