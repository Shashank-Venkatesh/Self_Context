"""Native-style command line interface for Self Context."""

from __future__ import annotations

import json
import sys

import click

from .config import AppConfig
from .core.retrieval import RetrievalService
from .core.storage import ContextStore
from .sources.email.ingestion import EmailIngestor
from .sources.email.providers import GmailProvider, build_domain_query


def _config() -> AppConfig:
    config = AppConfig.from_environment()
    config.ensure_directories()
    return config


def _store(config: AppConfig) -> ContextStore:
    return ContextStore(config.database_path)


@click.group()
@click.version_option()
def main() -> None:
    """Local-first personal context for AI."""


@main.command()
def init() -> None:
    """Create Self Context's local configuration and data directories."""
    config = _config()
    store = _store(config)
    store.close()
    click.echo(f"Initialized Self Context in {config.data_dir}")


@main.command()
def config() -> None:
    """Show non-sensitive local paths and configuration state."""
    current = _config()
    click.echo(f"config_dir: {current.config_dir}")
    click.echo(f"data_dir: {current.data_dir}")
    click.echo(f"database: {current.database_path}")
    credential_state = "configured" if current.gmail_credentials_path else "not configured"
    click.echo(f"gmail_credentials: {credential_state}")


@main.group()
def auth() -> None:
    """Authenticate an external source."""


@auth.command("gmail")
def auth_gmail() -> None:
    """Complete the official Gmail OAuth flow in a browser."""
    current = _config()
    try:
        GmailProvider(current.gmail_credentials_path, current.gmail_token_path).authenticate()
    except RuntimeError as error:
        raise click.ClickException(str(error)) from error
    click.echo("Gmail authentication completed.")


@main.group()
def sync() -> None:
    """Synchronize configured sources into local storage."""


@sync.command("email")
@click.option("--query", default=None, help="Optional Gmail search query.")
@click.option("--domain", "domains", multiple=True, help="Only sync emails involving this domain. Repeatable.")
def sync_email(query: str | None, domains: tuple[str, ...]) -> None:
    """Fetch, normalize, and index Gmail messages locally."""
    current = _config()
    store = _store(current)
    try:
        provider = GmailProvider(current.gmail_credentials_path, current.gmail_token_path)
        count = EmailIngestor(provider, store).sync(build_domain_query(domains, query))
    except ValueError as error:
        raise click.ClickException(str(error)) from error
    except Exception as error:
        raise click.ClickException(str(error)) from error
    finally:
        store.close()
    click.echo(f"Synchronized {count} email message(s).")


@main.command()
@click.argument("query")
@click.option("--source", default=None)
@click.option("--type", "item_type", default=None)
def search(query: str, source: str | None, item_type: str | None) -> None:
    """Search indexed context."""
    store = _store(_config())
    try:
        items = RetrievalService(store).search_context(query, source=source, type=item_type)
        for item in items:
            click.echo(f"{item.id}\t{item.title}")
    finally:
        store.close()


@main.command("get")
@click.argument("item_id")
def get_item(item_id: str) -> None:
    """Print one indexed context item as JSON."""
    store = _store(_config())
    try:
        item = RetrievalService(store).get_context_item(item_id)
    finally:
        store.close()
    if not item:
        raise click.ClickException(f"Context item not found: {item_id}")
    click.echo(json.dumps(item.to_dict(), indent=2))


@main.command()
def status() -> None:
    """Show local index status."""
    current = _config()
    store = _store(current)
    try:
        count = store.count()
    finally:
        store.close()
    click.echo(f"database: {current.database_path}")
    click.echo(f"items: {count}")


@main.command()
def mcp() -> None:
    """Start the local MCP server over stdio."""
    from .mcp.server import run_server
    run_server(_config())


if __name__ == "__main__":
    main(sys.argv[1:])