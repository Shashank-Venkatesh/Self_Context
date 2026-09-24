import base64
from datetime import timezone

from self_context.sources.email.ingestion import EmailIngestor
from self_context.sources.email.normalization import normalize_gmail_message
from self_context.sources.email.providers import GmailProvider, build_domain_query


def encoded(value: str) -> str:
    return base64.urlsafe_b64encode(value.encode()).decode()


def message(message_id: str, payload: dict, page: str = "INBOX") -> dict:
    payload.setdefault("headers", [
        {"name": "From", "value": "Ada <ada@example.com>"},
        {"name": "To", "value": "me@example.com"},
        {"name": "Subject", "value": "Project update"},
        {"name": "Date", "value": "Mon, 01 Jan 2024 12:00:00 +0000"},
    ])
    return {"id": message_id, "threadId": "thread-1", "labelIds": [page], "payload": payload}


def test_normalizes_plain_html_and_multipart():
    plain = normalize_gmail_message(message("plain", {"mimeType": "text/plain", "body": {"data": encoded("hello plain")}}))
    assert plain.body == "hello plain"
    html = normalize_gmail_message(message("html", {"mimeType": "text/html", "body": {"data": encoded("<p>Hello <b>HTML</b></p>")}}))
    assert html.body == "Hello HTML"
    multipart = normalize_gmail_message(message("multi", {"mimeType": "multipart/alternative", "parts": [
        {"mimeType": "text/plain", "body": {"data": encoded("plain wins")}},
        {"mimeType": "text/html", "body": {"data": encoded("<p>html fallback</p>")}},
    ]}))
    assert multipart.body == "plain wins"
    assert multipart.timestamp.tzinfo == timezone.utc


class FakeProvider:
    def __init__(self, pages):
        self.pages = pages

    def fetch_messages(self, query=None):
        for page in self.pages:
            yield from page


def test_ingestion_handles_pagination_and_repeat_sync(store):
    messages = [[message("a", {"mimeType": "text/plain", "body": {"data": encoded("first")}})],
                [message("b", {"mimeType": "text/plain", "body": {"data": encoded("second")}})]]
    ingestor = EmailIngestor(FakeProvider(messages), store)
    assert ingestor.sync() == 2
    assert ingestor.sync() == 2
    assert store.count() == 2
    assert store.get_by_source("email", "a").content == "first"


class FakeMessages:
    def __init__(self):
        self.pages = [{"messages": [{"id": "a"}], "nextPageToken": "next"}, {"messages": [{"id": "b"}]}]
        self.page = 0

    def list(self, **kwargs):
        return self

    def list_next(self, request, response):
        self.page += 1
        return self if self.page < len(self.pages) else None

    def execute(self):
        return self.pages[self.page]

    def get(self, **kwargs):
        return FakeGet(kwargs["id"])


class FakeGet:
    def __init__(self, message_id):
        self.message_id = message_id

    def execute(self):
        return {"id": self.message_id, "payload": {"headers": []}}


class FakeUsers:
    def __init__(self):
        self.messages_api = FakeMessages()

    def messages(self):
        return self.messages_api


class FakeService:
    def __init__(self):
        self.users_api = FakeUsers()

    def users(self):
        return self.users_api


def test_gmail_provider_uses_mocked_paginated_api():
    provider = GmailProvider(None, "/tmp/unused-token.json")
    provider._service = FakeService()
    messages = list(provider.fetch_messages("in:anywhere"))
    assert [message["id"] for message in messages] == ["a", "b"]


def test_domain_query_is_restrictive_and_composable():
    query = build_domain_query(["@Company.com", "partners.example"], "newer_than:30d")
    assert query == (
        "(newer_than:30d) AND (from:(*@company.com) OR to:(*@company.com) OR "
        "cc:(*@company.com) OR bcc:(*@company.com) OR from:(*@partners.example) OR "
        "to:(*@partners.example) OR cc:(*@partners.example) OR bcc:(*@partners.example))"
    )


def test_domain_query_rejects_invalid_domains():
    try:
        build_domain_query(["not a domain"])
    except ValueError as error:
        assert "Invalid email domain" in str(error)
    else:
        raise AssertionError("invalid domain was accepted")