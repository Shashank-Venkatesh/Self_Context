"""Normalized web page model independent of any web provider."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class NormalizedWebPage:
    url: str
    canonical_url: str
    title: str
    text: str
    fetched_at: datetime
    metadata: dict[str, Any] = field(default_factory=dict)
