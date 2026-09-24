"""Filesystem and environment configuration using Linux XDG conventions."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _xdg(name: str, fallback: Path) -> Path:
    return Path(os.environ.get(name, fallback)).expanduser()


@dataclass(frozen=True)
class AppConfig:
    config_dir: Path
    data_dir: Path
    cache_dir: Path
    database_path: Path
    gmail_credentials_path: Path | None
    gmail_token_path: Path

    @classmethod
    def from_environment(cls) -> "AppConfig":
        home = Path.home()
        config_dir = _xdg("XDG_CONFIG_HOME", home / ".config") / "self-context"
        data_dir = _xdg("XDG_DATA_HOME", home / ".local" / "share") / "self-context"
        cache_dir = _xdg("XDG_CACHE_HOME", home / ".cache") / "self-context"
        configured_credentials = os.environ.get("SELF_CONTEXT_GMAIL_CREDENTIALS")
        credentials = Path(configured_credentials).expanduser() if configured_credentials else None
        return cls(config_dir, data_dir, cache_dir, data_dir / "context.sqlite3", credentials,
                   config_dir / "gmail-token.json")

    def ensure_directories(self) -> None:
        for directory in (self.config_dir, self.data_dir, self.cache_dir):
            directory.mkdir(parents=True, exist_ok=True)