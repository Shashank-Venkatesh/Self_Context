"""Data models for local markdown and text file context sources."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class FileDocument:
    """Represents a scanned markdown or text file document."""

    path: str
    relative_path: str
    file_type: str
    title: str
    content: str
    size: int
    mtime: datetime
    checksum: str
    metadata: dict[str, Any] = field(default_factory=dict)
