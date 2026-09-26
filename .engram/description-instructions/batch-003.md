# Node Description Batch 4 of 4

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

- "email_normalization_textextractor_init": ".__init__()" | kind=code-symbol | source=src/self_context/sources/email/normalization.py:L15 | neighbors=[_TextExtractor]
- "email_providers_emailprovider_authenticate": ".authenticate()" | kind=code-symbol | source=src/self_context/sources/email/providers.py:L15 | neighbors=[EmailProvider]
- "email_providers_emailprovider_fetch_messages": ".fetch_messages()" | kind=code-symbol | source=src/self_context/sources/email/providers.py:L18 | neighbors=[EmailProvider]
- "email_providers_emailprovider_get_message": ".get_message()" | kind=code-symbol | source=src/self_context/sources/email/providers.py:L17 | neighbors=[EmailProvider]
- "email_providers_emailprovider_list_messages": ".list_messages()" | kind=code-symbol | source=src/self_context/sources/email/providers.py:L16 | neighbors=[EmailProvider]
- "email_providers_gmailprovider_authenticate": ".authenticate()" | kind=code-symbol | source=src/self_context/sources/email/providers.py:L29 | neighbors=[GmailProvider]
- "email_providers_gmailprovider_decode_body": ".decode_body()" | kind=code-symbol | source=src/self_context/sources/email/providers.py:L74 | neighbors=[GmailProvider]
- "email_providers_gmailprovider_fetch_messages": ".fetch_messages()" | kind=code-symbol | source=src/self_context/sources/email/providers.py:L51 | neighbors=[GmailProvider]
- "email_providers_gmailprovider_get_message": ".get_message()" | kind=code-symbol | source=src/self_context/sources/email/providers.py:L66 | neighbors=[GmailProvider]
- "email_providers_gmailprovider_init": ".__init__()" | kind=code-symbol | source=src/self_context/sources/email/providers.py:L24 | neighbors=[GmailProvider]
- "email_providers_gmailprovider_list_messages": ".list_messages()" | kind=code-symbol | source=src/self_context/sources/email/providers.py:L57 | neighbors=[GmailProvider]
- "email_providers_parse_header": "parse_header()" | kind=code-symbol | source=src/self_context/sources/email/providers.py:L80 | neighbors=[providers.py]
- "email_providers_parse_timestamp": "parse_timestamp()" | kind=code-symbol | source=src/self_context/sources/email/providers.py:L84 | neighbors=[providers.py]
- "email_providers_rationale_1": "Email provider interfaces and the official Gmail API implementation." | kind=entity | source=src/self_context/sources/email/providers.py:L1 | neighbors=[providers.py]
- "email_providers_rationale_90": "Build a Gmail search query restricted to selected email domains." | kind=entity | source=src/self_context/sources/email/providers.py:L90 | neighbors=[build_domain_query()]
- "htmlparser": "HTMLParser" | kind=code-symbol | neighbors=[_TextExtractor]
- "mcp_init_rationale_1": "Model Context Protocol integration." | kind=entity | source=src/self_context/mcp/__init__.py:L1 | neighbors=[__init__.py]
- "mcp_server_rationale_1": "Local stdio MCP server exposing context-oriented operations." | kind=entity | source=src/self_context/mcp/server.py:L1 | neighbors=[server.py]
- "protocol": "Protocol" | kind=code-symbol | neighbors=[EmailProvider]
- "self_context_config_appconfig_ensure_directories": ".ensure_directories()" | kind=code-symbol | source=src/self_context/config.py:L34 | neighbors=[AppConfig]
- "self_context_config_rationale_1": "Filesystem and environment configuration using Linux XDG conventions." | kind=entity | source=src/self_context/config.py:L1 | neighbors=[config.py]
- "self_context_init_rationale_1": "Self Context: a local-first personal context library for AI." | kind=entity | source=src/self_context/__init__.py:L1 | neighbors=[__init__.py]
- "sources_init_rationale_1": "External context source integrations." | kind=entity | source=src/self_context/sources/__init__.py:L1 | neighbors=[__init__.py]
- "tests_conftest_store": "store()" | kind=code-symbol | source=tests/conftest.py:L9 | neighbors=[conftest.py]
- "tests_test_cli_test_sync_email_help_describes_domain_filter": "test_sync_email_help_describes_domain_filter()" | kind=code-symbol | source=tests/test_cli.py:L6 | neighbors=[test_cli.py]
- "tests_test_email_fakeget_execute": ".execute()" | kind=code-symbol | source=tests/test_email.py:L78 | neighbors=[FakeGet]
- "tests_test_email_fakeget_init": ".__init__()" | kind=code-symbol | source=tests/test_email.py:L75 | neighbors=[FakeGet]
- "tests_test_email_fakemessages_execute": ".execute()" | kind=code-symbol | source=tests/test_email.py:L67 | neighbors=[FakeMessages]
- "tests_test_email_fakemessages_init": ".__init__()" | kind=code-symbol | source=tests/test_email.py:L56 | neighbors=[FakeMessages]
- "tests_test_email_fakemessages_list": ".list()" | kind=code-symbol | source=tests/test_email.py:L60 | neighbors=[FakeMessages]
- "tests_test_email_fakemessages_list_next": ".list_next()" | kind=code-symbol | source=tests/test_email.py:L63 | neighbors=[FakeMessages]
- "tests_test_email_fakeprovider_init": ".__init__()" | kind=code-symbol | source=tests/test_email.py:L37 | neighbors=[FakeProvider]
- "tests_test_email_fakeservice_users": ".users()" | kind=code-symbol | source=tests/test_email.py:L94 | neighbors=[FakeService]
- "tests_test_email_fakeusers_messages": ".messages()" | kind=code-symbol | source=tests/test_email.py:L86 | neighbors=[FakeUsers]
- "tests_test_email_test_domain_query_is_restrictive_and_composable": "test_domain_query_is_restrictive_and_composable()" | kind=code-symbol | source=tests/test_email.py:L105 | neighbors=[test_email.py]
- "tests_test_email_test_domain_query_rejects_invalid_domains": "test_domain_query_rejects_invalid_domains()" | kind=code-symbol | source=tests/test_email.py:L114 | neighbors=[test_email.py]
- "tests_test_mcp_test_mcp_context_tools_search_and_get": "test_mcp_context_tools_search_and_get()" | kind=code-symbol | source=tests/test_mcp.py:L8 | neighbors=[test_mcp.py]

## Instructions

Write a single JSON object mapping each node id to a one-sentence description
to: /home/scatterzz/Documents/Projects/Self_Context/.engram/description-instructions/batch-003.json

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
