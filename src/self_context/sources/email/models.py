"""Normalized email model independent of any email provider."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class NormalizedEmail:
    message_id: str
    thread_id: str | None
    sender: str
    recipients: list[str]
    cc: list[str]
    bcc: list[str]
    subject: str
    timestamp: datetime
    body: str
    labels: list[str] = field(default_factory=list)