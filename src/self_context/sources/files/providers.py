"""File provider scanning local directories or single files for markdown and text files."""

from __future__ import annotations

import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Iterator

from .models import FileDocument

DEFAULT_ALLOWED_EXTENSIONS: set[str] = {".md", ".markdown", ".txt", ".rst", ".org"}
DEFAULT_IGNORED_DIRS: set[str] = {".git", ".venv", "node_modules", "dist", "__pycache__"}


class LocalFileProvider:
    """Scans local filesystem directories or individual files for document ingestion."""

    def __init__(
        self,
        root_path: str | Path,
        allowed_extensions: Iterable[str] | None = None,
        ignored_dirs: Iterable[str] | None = None,
    ) -> None:
        self.root_path = Path(root_path).expanduser().resolve()
        if allowed_extensions is not None:
            self.allowed_extensions = {
                ext.lower() if ext.startswith(".") else f".{ext.lower()}"
                for ext in allowed_extensions
            }
        else:
            self.allowed_extensions = set(DEFAULT_ALLOWED_EXTENSIONS)

        self.ignored_dirs = (
            set(ignored_dirs) if ignored_dirs is not None else set(DEFAULT_IGNORED_DIRS)
        )

    def scan_files(self) -> Iterator[FileDocument]:
        """Scan configured root path and yield FileDocument objects."""
        if not self.root_path.exists():
            return

        if self.root_path.is_file():
            doc = self._process_file(self.root_path, relative_to=self.root_path.parent)
            if doc:
                yield doc
            return

        for dirpath, dirnames, filenames in os.walk(self.root_path):
            dirnames[:] = [
                d for d in dirnames
                if not d.startswith(".") and d not in self.ignored_dirs
            ]

            for filename in filenames:
                if filename.startswith("."):
                    continue
                file_path = Path(dirpath) / filename
                if file_path.suffix.lower() in self.allowed_extensions:
                    doc = self._process_file(file_path, relative_to=self.root_path)
                    if doc:
                        yield doc

    def __iter__(self) -> Iterator[FileDocument]:
        return self.scan_files()

    def _process_file(self, file_path: Path, relative_to: Path) -> FileDocument | None:
        try:
            stat = file_path.stat()
            content = self._read_content(file_path)
            try:
                relative_path = str(file_path.relative_to(relative_to))
            except ValueError:
                relative_path = file_path.name

            mtime = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
            checksum = hashlib.sha256(content.encode("utf-8")).hexdigest()
            file_type = file_path.suffix.lower()

            return FileDocument(
                path=str(file_path),
                relative_path=relative_path,
                file_type=file_type,
                title=file_path.stem,
                content=content,
                size=stat.st_size,
                mtime=mtime,
                checksum=checksum,
            )
        except Exception:
            return None

    @staticmethod
    def _read_content(file_path: Path) -> str:
        """Safely read file content using UTF-8 with fallback decoding."""
        try:
            return file_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, Exception):
            try:
                return file_path.read_text(encoding="latin-1")
            except Exception:
                try:
                    return file_path.read_bytes().decode("utf-8", errors="replace")
                except Exception:
                    return ""
