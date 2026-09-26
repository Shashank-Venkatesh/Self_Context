# Node Description Batch 3 of 4

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
Write every description in English (en). Do not switch languages.
No marketing language.
Respond ONLY with a JSON object mapping each node id (as a string) to its
one-sentence description — no prose, no markdown fences.

- "self_context_cli_rationale_1": "Native-style command line interface for Self Context." | kind=entity | source=src/self_context/cli.py:L1 | neighbors=[cli.py, AppConfig]
- "self_context_cli_rationale_111": "Print one indexed context item as JSON." | kind=entity | source=src/self_context/cli.py:L111 | neighbors=[get_item(), AppConfig]
- "self_context_cli_rationale_124": "Show local index status." | kind=entity | source=src/self_context/cli.py:L124 | neighbors=[status(), AppConfig]
- "self_context_cli_rationale_137": "Start the local MCP server over stdio." | kind=entity | source=src/self_context/cli.py:L137 | neighbors=[mcp(), AppConfig]
- "self_context_cli_rationale_30": "Local-first personal context for AI." | kind=entity | source=src/self_context/cli.py:L30 | neighbors=[main(), AppConfig]
- "self_context_cli_rationale_35": "Create Self Context's local configuration and data directories." | kind=entity | source=src/self_context/cli.py:L35 | neighbors=[init(), AppConfig]
- "self_context_cli_rationale_44": "Show non-sensitive local paths and configuration state." | kind=entity | source=src/self_context/cli.py:L44 | neighbors=[_config(), AppConfig]
- "self_context_cli_rationale_55": "Authenticate an external source." | kind=entity | source=src/self_context/cli.py:L55 | neighbors=[auth(), AppConfig]
- "self_context_cli_rationale_60": "Complete the official Gmail OAuth flow in a browser." | kind=entity | source=src/self_context/cli.py:L60 | neighbors=[auth_gmail(), AppConfig]
- "self_context_cli_rationale_71": "Synchronize configured sources into local storage." | kind=entity | source=src/self_context/cli.py:L71 | neighbors=[sync(), AppConfig]
- "self_context_cli_rationale_78": "Fetch, normalize, and index Gmail messages locally." | kind=entity | source=src/self_context/cli.py:L78 | neighbors=[sync_email(), AppConfig]
- "self_context_cli_rationale_98": "Search indexed context." | kind=entity | source=src/self_context/cli.py:L98 | neighbors=[search(), AppConfig]
- "self_context_config_appconfig_from_environment": ".from_environment()" | kind=code-symbol | source=src/self_context/config.py:L24 | neighbors=[AppConfig, _xdg()]
- "self_context_config_xdg": "_xdg()" | kind=code-symbol | source=src/self_context/config.py:L10 | neighbors=[config.py, .from_environment()]
- "self_context_init": "__init__.py" | kind=code-symbol | source=src/self_context/__init__.py:L1 | neighbors=[080e01a Foundational Layout has been set, Self Context: a local-first personal co…]
- "sources_init": "__init__.py" | kind=code-symbol | source=src/self_context/sources/__init__.py:L1 | neighbors=[080e01a Foundational Layout has been set, External context source integrations.]
- "tests_conftest": "conftest.py" | kind=code-symbol | source=tests/conftest.py:L1 | neighbors=[080e01a Foundational Layout has been set, store()]
- "tests_test_core_test_search_and_source_filter": "test_search_and_source_filter()" | kind=code-symbol | source=tests/test_core.py:L26 | neighbors=[test_core.py, item()]
- "tests_test_core_test_store_crud_and_duplicate_upsert": "test_store_crud_and_duplicate_upsert()" | kind=code-symbol | source=tests/test_core.py:L12 | neighbors=[test_core.py, item()]
- "tests_test_email_fakemessages_get": ".get()" | kind=code-symbol | source=tests/test_email.py:L70 | neighbors=[FakeMessages, FakeGet]
- "tests_test_email_fakeprovider_fetch_messages": ".fetch_messages()" | kind=code-symbol | source=tests/test_email.py:L40 | neighbors=[FakeProvider, test_gmail_provider_uses_mocked_paginat…]
- "tests_test_email_fakeservice_init": ".__init__()" | kind=code-symbol | source=tests/test_email.py:L91 | neighbors=[FakeService, FakeUsers]
- "tests_test_email_fakeusers_init": ".__init__()" | kind=code-symbol | source=tests/test_email.py:L83 | neighbors=[FakeUsers, FakeMessages]
- "tests_test_mcp": "test_mcp.py" | kind=code-symbol | source=tests/test_mcp.py:L1 | neighbors=[080e01a Foundational Layout has been set, test_mcp_context_tools_search_and_get()]
- "core_init_rationale_1": "Core domain, storage, and retrieval services." | kind=entity | source=src/self_context/core/__init__.py:L1 | neighbors=[__init__.py]
- "core_models_contextitem_to_dict": ".to_dict()" | kind=code-symbol | source=src/self_context/core/models.py:L28 | neighbors=[ContextItem]
- "core_models_encode_metadata": "encode_metadata()" | kind=code-symbol | source=src/self_context/core/models.py:L35 | neighbors=[models.py]
- "core_models_parse_datetime": "parse_datetime()" | kind=code-symbol | source=src/self_context/core/models.py:L39 | neighbors=[models.py]
- "core_models_rationale_1": "Source-independent context domain models." | kind=entity | source=src/self_context/core/models.py:L1 | neighbors=[models.py]
- "core_models_utc_now": "utc_now()" | kind=code-symbol | source=src/self_context/core/models.py:L11 | neighbors=[models.py]
- "core_retrieval_retrievalservice_get_context_item": ".get_context_item()" | kind=code-symbol | source=src/self_context/core/retrieval.py:L15 | neighbors=[RetrievalService]
- "core_retrieval_retrievalservice_init": ".__init__()" | kind=code-symbol | source=src/self_context/core/retrieval.py:L8 | neighbors=[RetrievalService]
- "core_storage_contextstore_close": ".close()" | kind=code-symbol | source=src/self_context/core/storage.py:L39 | neighbors=[ContextStore]
- "core_storage_contextstore_count": ".count()" | kind=code-symbol | source=src/self_context/core/storage.py:L113 | neighbors=[ContextStore]
- "core_storage_contextstore_delete": ".delete()" | kind=code-symbol | source=src/self_context/core/storage.py:L85 | neighbors=[ContextStore]
- "email_ingestion_emailingestor_init": ".__init__()" | kind=code-symbol | source=src/self_context/sources/email/ingestion.py:L12 | neighbors=[EmailIngestor]
- "email_ingestion_emailingestor_sync": ".sync()" | kind=code-symbol | source=src/self_context/sources/email/ingestion.py:L16 | neighbors=[EmailIngestor]
- "email_init_rationale_1": "Email source integration." | kind=entity | source=src/self_context/sources/email/__init__.py:L1 | neighbors=[__init__.py]
- "email_models_rationale_1": "Normalized email model independent of any email provider." | kind=entity | source=src/self_context/sources/email/models.py:L1 | neighbors=[models.py]
- "email_normalization_textextractor_handle_data": ".handle_data()" | kind=code-symbol | source=src/self_context/sources/email/normalization.py:L19 | neighbors=[_TextExtractor]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /home/scatterzz/Documents/Projects/Self_Context/.engram/description-instructions/batch-002.json

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
