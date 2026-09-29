"""Filesystem and environment configuration using Linux XDG conventions."""

from __future__ import annotations

import json
import os
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path


def _xdg(name: str, fallback: Path) -> Path:
    return Path(os.environ.get(name, fallback)).expanduser()


def save_settings(
    config_dir: Path,
    *,
    data_dir: Path | str | None = None,
    gmail_credentials_path: Path | str | None = None,
    domains: Iterable[str] | None = None,
    last_sync: str | None = None,
) -> None:
    config_dir.mkdir(parents=True, exist_ok=True)
    settings_file = config_dir / "config.json"
    existing: dict[str, object] = {}
    if settings_file.exists():
        try:
            existing = json.loads(settings_file.read_text(encoding="utf-8"))
        except Exception:
            existing = {}
    if data_dir is not None:
        existing["data_dir"] = str(Path(data_dir).expanduser())
    if gmail_credentials_path is not None:
        existing["gmail_credentials_path"] = str(Path(gmail_credentials_path).expanduser())
    if domains is not None:
        existing["domains"] = list(domains)
    if last_sync is not None:
        existing["last_sync"] = str(last_sync)
    settings_file.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    settings_file.chmod(0o600)


@dataclass(frozen=True)
class AppConfig:
    config_dir: Path
    data_dir: Path
    cache_dir: Path
    database_path: Path
    gmail_credentials_path: Path | None
    gmail_token_path: Path
    saved_domains: tuple[str, ...] = ()
    last_sync: str | None = None

    @classmethod
    def from_environment(cls, data_dir: Path | str | None = None) -> "AppConfig":
        home = Path.home()
        config_dir = _xdg("XDG_CONFIG_HOME", home / ".config") / "self-context"

        settings_file = config_dir / "config.json"
        settings: dict[str, object] = {}
        if settings_file.exists():
            try:
                settings = json.loads(settings_file.read_text(encoding="utf-8"))
            except Exception:
                settings = {}

        if data_dir is not None:
            resolved_data_dir = Path(data_dir).expanduser()
        elif "XDG_DATA_HOME" in os.environ:
            resolved_data_dir = _xdg("XDG_DATA_HOME", home / ".local" / "share") / "self-context"
        elif settings.get("data_dir"):
            resolved_data_dir = Path(str(settings["data_dir"])).expanduser()
        else:
            resolved_data_dir = home / ".local" / "share" / "self-context"

        cache_dir = _xdg("XDG_CACHE_HOME", home / ".cache") / "self-context"

        configured_credentials = os.environ.get("SELF_CONTEXT_GMAIL_CREDENTIALS") or settings.get("gmail_credentials_path")
        credentials = Path(str(configured_credentials)).expanduser() if configured_credentials else None

        raw_domains = settings.get("domains")
        saved_domains = tuple(raw_domains) if isinstance(raw_domains, list) else ()
        last_sync = str(settings["last_sync"]) if settings.get("last_sync") else None

        return cls(
            config_dir,
            resolved_data_dir,
            cache_dir,
            resolved_data_dir / "context.sqlite3",
            credentials,
            config_dir / "gmail-token.json",
            saved_domains,
            last_sync,
        )

    def ensure_directories(self) -> None:
        for directory in (self.config_dir, self.data_dir, self.cache_dir):
            directory.mkdir(parents=True, exist_ok=True)