"""Email provider interfaces and the official Gmail API implementation."""

from __future__ import annotations

import base64
import email.utils
import re
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol


class EmailProvider(Protocol):
    def authenticate(self) -> None: ...
    def list_messages(self, query: str | None = None) -> Iterable[dict[str, Any]]: ...
    def get_message(self, message_id: str) -> dict[str, Any]: ...
    def fetch_messages(self, query: str | None = None) -> Iterable[dict[str, Any]]: ...


class GmailProvider:
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

    def __init__(self, credentials_path: str | Path | None, token_path: str | Path):
        self.credentials_path = Path(credentials_path).expanduser() if credentials_path else None
        self.token_path = Path(token_path).expanduser()
        self._service: Any = None

    def authenticate(self) -> None:
        if not self.credentials_path or not self.credentials_path.exists():
            raise RuntimeError("Gmail OAuth is not configured. Set SELF_CONTEXT_GMAIL_CREDENTIALS.")
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow

        credentials = None
        if self.token_path.exists():
            credentials = Credentials.from_authorized_user_file(str(self.token_path), self.SCOPES)
        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(str(self.credentials_path), self.SCOPES)
                credentials = flow.run_local_server(port=0)
            self.token_path.parent.mkdir(parents=True, exist_ok=True)
            self.token_path.write_text(credentials.to_json(), encoding="utf-8")
            self.token_path.chmod(0o600)
        from googleapiclient.discovery import build
        self._service = build("gmail", "v1", credentials=credentials, cache_discovery=False)

    def fetch_messages(self, query: str | None = None) -> Iterable[dict[str, Any]]:
        if not self._service:
            self.authenticate()
        for message in self.list_messages(query):
            yield self.get_message(message["id"])

    def list_messages(self, query: str | None = None) -> Iterable[dict[str, Any]]:
        if not self._service:
            self.authenticate()
        request = self._service.users().messages().list(userId="me", q=query or "", maxResults=100)
        while request is not None:
            response = request.execute()
            yield from response.get("messages", [])
            request = self._service.users().messages().list_next(request, response)

    def get_message(self, message_id: str) -> dict[str, Any]:
        if not self._service:
            self.authenticate()
        return self._service.users().messages().get(
            userId="me", id=message_id, format="full"
        ).execute()

    @staticmethod
    def decode_body(data: str | None) -> str:
        if not data:
            return ""
        return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4)).decode("utf-8", errors="replace")


def parse_header(headers: list[dict[str, str]], name: str) -> str:
    return next((h.get("value", "") for h in headers if h.get("name", "").lower() == name.lower()), "")


def parse_timestamp(value: str) -> datetime:
    parsed = email.utils.parsedate_to_datetime(value) if value else None
    return (parsed or datetime.now(timezone.utc)).astimezone(timezone.utc)


def build_domain_query(domains: Iterable[str], query: str | None = None) -> str | None:
    """Build a Gmail search query restricted to selected email domains."""
    normalized_domains: list[str] = []
    for domain in domains:
        normalized = domain.strip().lower().lstrip("@")
        if not re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)+", normalized):
            raise ValueError(f"Invalid email domain: {domain}")
        if normalized not in normalized_domains:
            normalized_domains.append(normalized)
    if not normalized_domains:
        return query
    domain_terms = " OR ".join(
        f"from:(*@{domain}) OR to:(*@{domain}) OR cc:(*@{domain}) OR bcc:(*@{domain})"
        for domain in normalized_domains
    )
    domain_query = f"({domain_terms})"
    return f"({query}) AND {domain_query}" if query else domain_query