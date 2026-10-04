# Graph Report - .  (2026-09-26)

## Corpus Check
- Corpus is ~5,912 words - fits in a single context window. You may not need a graph.

## Summary
- 157 nodes · 248 edges · 9 communities detected
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 34 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output
- Edge kinds: contains: 52 · method: 48 · calls: 42 · uses: 34 · rationale_for: 27 · MODIFIES: 20 · ON_BRANCH: 12 · imports_from: 7 · PARENT_OF: 4 · inherits: 2


## Input Scope
- Requested: auto
- Resolved: committed (source: default-auto)
- Included files: 24 · Candidates: 28
- Excluded: 8 untracked · 6038 ignored · 0 sensitive · 0 missing committed
- Recommendation: Use --scope all or graphify.yaml inputs.corpus for a knowledge-base folder.

## Graph Freshness
- Built from Git commit: `7b22d8e`
- Compare this hash to `git rev-parse HEAD` before trusting freshness-sensitive graph output.
## God Nodes (most connected - your core abstractions)
1. `ContextStore` - 17 edges
2. `AppConfig` - 15 edges
3. `GmailProvider` - 14 edges
4. `_config()` - 9 edges
5. `EmailIngestor` - 9 edges
6. `FakeMessages` - 9 edges
7. `_TextExtractor` - 8 edges
8. `EmailProvider` - 8 edges
9. `RetrievalService` - 7 edges
10. `_store()` - 6 edges

## Surprising Connections (you probably didn't know these)
- `FakeGet` --uses--> `EmailIngestor`  [INFERRED]
  tests/test_email.py → src/self_context/sources/email/ingestion.py
- `FakeMessages` --uses--> `EmailIngestor`  [INFERRED]
  tests/test_email.py → src/self_context/sources/email/ingestion.py
- `FakeProvider` --uses--> `EmailIngestor`  [INFERRED]
  tests/test_email.py → src/self_context/sources/email/ingestion.py
- `FakeService` --uses--> `EmailIngestor`  [INFERRED]
  tests/test_email.py → src/self_context/sources/email/ingestion.py
- `FakeUsers` --uses--> `EmailIngestor`  [INFERRED]
  tests/test_email.py → src/self_context/sources/email/ingestion.py

## Communities

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (11): GmailProvider, encoded(), FakeGet, FakeMessages, FakeProvider, FakeService, FakeUsers, message() (+3 more)

### Community 1 - "Community 1"
Cohesion: 0.12
Nodes (27): auth(), auth_gmail(), _config(), get_item(), init(), main(), mcp(), Native-style command line interface for Self Context. (+19 more)

### Community 2 - "Community 2"
Cohesion: 0.12
Nodes (13): Documentation, Foundation, main, 080e01a Foundational Layout has been set, 47aeaa5 Initial commit, 7b22d8e Foundational Documentation added to the code base, d1fd9cf Readme File update, e9af453 Add MIT License to the project (+5 more)

### Community 3 - "Community 3"
Cohesion: 0.13
Nodes (5): Source-independent context domain models., EmailIngestor, Email ingestion pipeline: fetch, normalize, map, and idempotently persist., EmailProvider, Protocol

### Community 4 - "Community 4"
Cohesion: 0.17
Nodes (7): ContextItem, Retrieval service that keeps callers independent of the storage engine., RetrievalService, SQLite-backed storage hidden behind a small context store API., create_server(), Local stdio MCP server exposing context-oriented operations., run_server()

### Community 5 - "Community 5"
Cohesion: 0.24
Nodes (1): ContextStore

### Community 6 - "Community 6"
Cohesion: 0.21
Nodes (9): NormalizedEmail, Normalized email model independent of any email provider., _body(), decoded_header(), normalize_gmail_message(), Convert Gmail message payloads into readable normalized email records., readable_html(), _TextExtractor (+1 more)

### Community 7 - "Community 7"
Cohesion: 0.33
Nodes (3): build_domain_query(), Email provider interfaces and the official Gmail API implementation., Build a Gmail search query restricted to selected email domains.

### Community 8 - "Community 8"
Cohesion: 0.83
Nodes (3): item(), test_search_and_source_filter(), test_store_crud_and_duplicate_upsert()

## Knowledge Gaps
- **11 isolated node(s):** `Self Context: a local-first personal context library for AI.`, `Filesystem and environment configuration using Linux XDG conventions.`, `Core domain, storage, and retrieval services.`, `Source-independent context domain models.`, `Model Context Protocol integration.` (+6 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 5`** (1 nodes): `ContextStore`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ContextStore` connect `Community 5` to `Community 4`?**
  _High betweenness centrality (0.162) - this node is a cross-community bridge._
- **Why does `GmailProvider` connect `Community 0` to `Community 6`, `Community 7`?**
  _High betweenness centrality (0.123) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `ContextStore` (e.g. with `Retrieval service that keeps callers independent of the storage engine.` and `RetrievalService`) actually correct?**
  _`ContextStore` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `AppConfig` (e.g. with `Native-style command line interface for Self Context.` and `Print one indexed context item as JSON.`) actually correct?**
  _`AppConfig` has 12 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `GmailProvider` (e.g. with `Convert Gmail message payloads into readable normalized email records.` and `_TextExtractor`) actually correct?**
  _`GmailProvider` has 7 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Self Context: a local-first personal context library for AI.`, `Filesystem and environment configuration using Linux XDG conventions.`, `Core domain, storage, and retrieval services.` to the rest of the system?**
  _11 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.08712121212121213 - nodes in this community are weakly interconnected._