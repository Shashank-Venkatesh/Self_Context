"""Source-independent context domain models."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class ContextItem:
    id: str
    source: str
    source_id: str
    type: str
    title: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    indexed_at: datetime = field(default_factory=utc_now)

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        for key in ("created_at", "updated_at", "indexed_at"):
            value[key] = value[key].isoformat()
        return value


def encode_metadata(metadata: dict[str, Any]) -> str:
    return json.dumps(metadata, separators=(",", ":"), sort_keys=True)


def parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))