"""Local stdio MCP server exposing context-oriented operations."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from ..config import AppConfig
from ..core.retrieval import RetrievalService
from ..core.storage import ContextStore


def create_server(retrieval: RetrievalService) -> FastMCP:
    server = FastMCP("self-context")

    @server.tool()
    def search_context(query: str, source: str | None = None, type: str | None = None) -> list[dict[str, Any]]:
        """Search locally indexed context by keyword, optionally filtered by source or type."""
        return [item.to_dict() for item in retrieval.search_context(query, source=source, type=type)]

    @server.tool()
    def get_context_item(item_id: str) -> dict[str, Any] | None:
        """Retrieve one locally indexed context item by its ID."""
        item = retrieval.get_context_item(item_id)
        return item.to_dict() if item else None

    @server.tool()
    def search_emails(query: str) -> list[dict[str, Any]]:
        """Search locally indexed email context."""
        return [item.to_dict() for item in retrieval.search_emails(query)]

    @server.resource("context://item/{item_id}")
    def context_item_resource(item_id: str) -> str:
        """Read-only resource view of one context item."""
        item = retrieval.get_context_item(item_id)
        if not item:
            raise ValueError(f"Context item not found: {item_id}")
        return str(item.to_dict())

    return server


def run_server(config: AppConfig | None = None) -> None:
    app_config = config or AppConfig.from_environment()
    app_config.ensure_directories()
    store = ContextStore(app_config.database_path)
    try:
        create_server(RetrievalService(store)).run(transport="stdio")
    finally:
        store.close()