"""Local markdown and text files context source plugin for Self Context."""

from .ingestion import FileIngestor
from .providers import LocalFileProvider

__all__ = ["LocalFileProvider", "FileIngestor"]
