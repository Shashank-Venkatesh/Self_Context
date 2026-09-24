"""Convert Gmail message payloads into readable normalized email records."""

from __future__ import annotations

import re
from email.header import decode_header, make_header
from html.parser import HTMLParser
from typing import Any

from .models import NormalizedEmail
from .providers import GmailProvider, parse_header, parse_timestamp


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)

    def text(self) -> str:
        return re.sub(r"\s+", " ", " ".join(self.parts)).strip()


def readable_html(value: str) -> str:
    parser = _TextExtractor()
    parser.feed(value)
    return parser.text()


def decoded_header(value: str) -> str:
    try:
        return str(make_header(decode_header(value)))
    except (LookupError, UnicodeError):
        return value


def _body(payload: dict[str, Any]) -> str:
    mime_type = payload.get("mimeType", "")
    data = payload.get("body", {}).get("data")
    if data and mime_type == "text/plain":
        return GmailProvider.decode_body(data).strip()
    if data and mime_type == "text/html":
        return readable_html(GmailProvider.decode_body(data))
    plain_parts: list[str] = []
    html_parts: list[str] = []
    for part in payload.get("parts", []):
        text = _body(part)
        if part.get("mimeType") == "text/html":
            html_parts.append(text)
        elif text:
            plain_parts.append(text)
    if plain_parts:
        return "\n\n".join(plain_parts).strip()
    if html_parts:
        return readable_html("\n".join(html_parts))
    if data:
        return GmailProvider.decode_body(data).strip()
    return ""


def normalize_gmail_message(message: dict[str, Any]) -> NormalizedEmail:
    payload = message.get("payload", {})
    headers = payload.get("headers", [])
    return NormalizedEmail(
        message_id=message["id"], thread_id=message.get("threadId"),
        sender=decoded_header(parse_header(headers, "From")),
        recipients=[part.strip() for part in parse_header(headers, "To").split(",") if part.strip()],
        cc=[part.strip() for part in parse_header(headers, "Cc").split(",") if part.strip()],
        bcc=[part.strip() for part in parse_header(headers, "Bcc").split(",") if part.strip()],
        subject=decoded_header(parse_header(headers, "Subject")) or "(no subject)",
        timestamp=parse_timestamp(parse_header(headers, "Date")), body=_body(payload),
        labels=message.get("labelIds", []),
    )