# Community Labeling

Engram is running in assistant/skill mode (no API key). You are the host
assistant (Claude Code / Codex / Gemini CLI). Read the community listing below
and write 2-5 word plain-language names for each.

## Language

Write every name in English (en). Do not switch languages.

## Communities

Community 0: GmailProvider, FakeMessages, .authenticate(, .decode_body(, .fetch_messages(, .get_message(, .__init__(, .list_messages(, test_email.py, encoded(, FakeGet, .execute(
Community 1: _config(, _store(, AppConfig, cli.py, auth(, auth_gmail(, get_item(, init(, main(, mcp(, Native-style command line interface for Self Context., Print one indexed context item as JSON.
Community 2: Documentation, Foundation, main, 080e01a Foundational Layout has been set, 47aeaa5 Initial commit, 7b22d8e Foundational Documentation added to the code base, d1fd9cf Readme File update, e9af453 Add MIT License to the project, __init__.py, Core domain, storage, and retrieval services., Email source integration., Model Context Protocol integration.
Community 3: EmailIngestor, EmailProvider, models.py, encode_metadata(, parse_datetime(, Source-independent context domain models., utc_now(, ingestion.py, .__init__(, .sync(, Email ingestion pipeline: fetch, normalize, map, and idempot, .authenticate(
Community 4: RetrievalService, ContextItem, .to_dict(, retrieval.py, Retrieval service that keeps callers independent of the stor, .get_context_item(, .__init__(, .search_context(, .search_emails(, storage.py, SQLite-backed storage hidden behind a small context store AP, server.py
Community 5: ContextStore, .add(, .add_many(, .close(, .count(, .delete(, ._from_row(, .get(, .get_by_source(, .__init__(, ._initialize(, .search(
Community 6: _TextExtractor, models.py, NormalizedEmail, Normalized email model independent of any email provider., normalization.py, _body(, decoded_header(, normalize_gmail_message(, Convert Gmail message payloads into readable normalized emai, readable_html(, .handle_data(, .__init__(
Community 7: providers.py, build_domain_query(, parse_header(, parse_timestamp(, Email provider interfaces and the official Gmail API impleme, Build a Gmail search query restricted to selected email doma
Community 8: test_core.py, item(, test_search_and_source_filter(, test_store_crud_and_duplicate_upsert(

## Instructions

Write a single JSON object mapping each community id (as a string) to its
2-5 word name to: /home/scatterzz/Documents/Projects/Self_Context/.engram/label-instructions/communities.json

Example:
```json
{
  "0": "Authentication Flow",
  "1": "Authentication Flow",
  "2": "Authentication Flow"
}
```

Then re-run `engram update` (or `engram label`) to ingest the names.
