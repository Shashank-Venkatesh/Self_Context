"""Native-style command line interface for Self Context."""

from __future__ import annotations

import base64
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import click

from .config import AppConfig, save_settings
from .core.retrieval import RetrievalService
from .core.storage import ContextStore
from .sources.email.ingestion import EmailIngestor
from .sources.email.providers import GmailProvider, build_domain_query
from .sources.files.ingestion import FileIngestor
from .sources.files.providers import LocalFileProvider
from .sources.web.ingestion import WebIngestor
from .sources.web.providers import HttpWebProvider


def _config(data_dir: Path | str | None = None) -> AppConfig:
    config = AppConfig.from_environment(data_dir=data_dir)
    config.ensure_directories()
    return config


def _store(config: AppConfig) -> ContextStore:
    return ContextStore(config.database_path)


def _is_interactive() -> bool:
    try:
        if sys.stdin and hasattr(sys.stdin, "isatty") and sys.stdin.isatty():
            return True
        if sys.stdin and type(sys.stdin).__module__.startswith("click.testing"):
            return True
    except Exception:
        pass
    return False


def _get_mcp_command() -> str:
    venv_cmd = Path(sys.executable).parent / "self-context"
    if venv_cmd.exists():
        return str(venv_cmd)
    which_cmd = shutil.which("self-context")
    if which_cmd:
        return which_cmd
    return f"{sys.executable} -m self_context.cli"


def _generate_mcp_links(command_path: str) -> tuple[str, str]:
    config_obj = {
        "mcpServers": {
            "self-context": {
                "command": command_path,
                "args": ["mcp"],
            }
        }
    }
    json_str = json.dumps(config_obj, indent=2)
    cursor_server_config = {
        "command": command_path,
        "args": ["mcp"],
    }
    encoded_config = base64.b64encode(json.dumps(cursor_server_config).encode("utf-8")).decode("utf-8")
    cursor_link = f"cursor://anysphere.cursor-deeplink/mcp/install?name=self-context&config={encoded_config}"
    return cursor_link, json_str


_MCP_CLIENT_CONFIG_PATHS = {
    "cursor": Path.home() / ".cursor" / "mcp.json",
    "claude": Path.home() / ".config" / "Claude" / "claude_desktop_config.json",
    "cline": (
        Path.home() / ".config" / "Code" / "User" / "globalStorage"
        / "saoudrizwan.claude-dev" / "settings" / "cline_mcp_settings.json"
    ),
}


def _install_mcp_config(client: str) -> Path:
    """Merge the self-context server entry into a client's MCP config file."""
    config_path = _MCP_CLIENT_CONFIG_PATHS[client]
    cmd_path = _get_mcp_command()
    _, json_str = _generate_mcp_links(cmd_path)
    new_config = json.loads(json_str)
    existing: dict[str, object] = {}
    if config_path.exists():
        try:
            existing = json.loads(config_path.read_text(encoding="utf-8"))
        except Exception as error:
            raise click.ClickException(f"Could not parse existing config at {config_path}: {error}") from error
    servers = existing.setdefault("mcpServers", {})
    if not isinstance(servers, dict):
        raise click.ClickException(f"Unexpected 'mcpServers' shape in {config_path}; not modifying it.")
    servers.update(new_config["mcpServers"])
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    return config_path


def _display_mcp_links(current: AppConfig) -> None:
    cmd_path = _get_mcp_command()
    cursor_link, json_config = _generate_mcp_links(cmd_path)
    click.echo("\n=== AI MCP Connection Configuration ===")
    click.echo("\n1. One-Click Install for Cursor:")
    click.echo(cursor_link)
    click.echo("\n2. Configuration JSON for Claude Desktop, Cline, and Cursor:")
    click.echo(json_config)
    click.echo("\nTo run the MCP server manually in terminal:")
    click.echo(f"{cmd_path} mcp\n")


@click.group()
@click.version_option()
def main() -> None:
    """Local-first personal context for AI."""


@main.command()
@click.option("--data-dir", "-d", type=click.Path(file_okay=False, path_type=Path), help="Directory where scraped data will live.")
def init(data_dir: Path | None) -> None:
    """Create Self Context's local configuration and data directories."""
    current = _config()
    if data_dir is None and _is_interactive():
        chosen = click.prompt(
            "Select directory where scraped data will live",
            default=str(current.data_dir),
            show_default=True,
        )
        data_dir = Path(chosen).expanduser()
    if data_dir is not None:
        save_settings(current.config_dir, data_dir=data_dir)
        current = _config(data_dir=data_dir)
    store = _store(current)
    store.close()
    click.echo(f"Initialized Self Context in {current.data_dir}")


@main.command()
@click.option("--data-dir", "-d", type=click.Path(file_okay=False, path_type=Path), help="Set directory where scraped data will live.")
def config(data_dir: Path | None) -> None:
    """Show or update non-sensitive local paths and configuration state."""
    current = _config()
    if data_dir is not None:
        save_settings(current.config_dir, data_dir=data_dir)
        current = _config(data_dir=data_dir)
        click.echo(f"Updated data directory to: {current.data_dir}")
    click.echo(f"config_dir: {current.config_dir}")
    click.echo(f"data_dir: {current.data_dir}")
    click.echo(f"database: {current.database_path}")
    credential_state = "configured" if current.gmail_credentials_path else "not configured"
    click.echo(f"gmail_credentials: {credential_state}")
    if current.saved_domains:
        click.echo(f"saved_domains: {', '.join(current.saved_domains)}")
    if current.last_sync:
        click.echo(f"last_sync: {current.last_sync}")


@main.group()
def auth() -> None:
    """Authenticate an external source."""


@auth.command("gmail")
@click.option("--credentials", "-c", type=click.Path(dir_okay=False, path_type=Path), help="Path to Google OAuth client secret JSON.")
def auth_gmail(credentials: Path | None) -> None:
    """Complete the official Gmail OAuth flow in a browser."""
    current = _config()
    creds_path = credentials or current.gmail_credentials_path
    if not creds_path:
        if _is_interactive():
            click.echo("Google OAuth client secret is not configured.")
            entered = click.prompt("Enter path to your client secret JSON file", type=str)
            creds_path = Path(entered).expanduser()
        else:
            raise click.ClickException("Gmail OAuth is not configured. Set SELF_CONTEXT_GMAIL_CREDENTIALS or use --credentials.")

    if not creds_path.exists():
        raise click.ClickException(f"Credentials file not found: {creds_path}")

    save_settings(current.config_dir, gmail_credentials_path=creds_path)
    try:
        provider = GmailProvider(creds_path, current.gmail_token_path)
        provider.authenticate()
        email_addr = None
        try:
            profile = provider.get_profile()
            email_addr = profile.get("emailAddress")
        except Exception:
            pass
        if email_addr:
            click.echo(f"Gmail authentication completed for {email_addr}.")
        else:
            click.echo("Gmail authentication completed.")
    except RuntimeError as error:
        raise click.ClickException(str(error)) from error


@main.group()
def sync() -> None:
    """Synchronize configured sources into local storage."""


@sync.command("email")
@click.option("--query", default=None, help="Optional Gmail search query.")
@click.option("--domain", "domains", multiple=True, help="Only sync emails involving this domain. Repeatable.")
@click.option("--all", "sync_all", is_flag=True, default=False, help="Sync all emails without asking for domain filter.")
def sync_email(query: str | None, domains: tuple[str, ...], sync_all: bool) -> None:
    """Fetch, normalize, and index Gmail messages locally."""
    current = _config()
    if not domains and not sync_all and _is_interactive():
        prompt_msg = "Enter domain to filter emails (e.g. company.com), or press Enter for all"
        if current.saved_domains:
            prompt_msg += f" [saved: {', '.join(current.saved_domains)}]"
        entered = click.prompt(prompt_msg, default="", show_default=False).strip()
        if entered:
            domains = tuple(d.strip() for d in re.split(r"[, ]+", entered) if d.strip())
        elif current.saved_domains:
            domains = current.saved_domains

    if domains:
        save_settings(current.config_dir, domains=domains)

    store = _store(current)
    try:
        provider = GmailProvider(current.gmail_credentials_path, current.gmail_token_path)
        count = EmailIngestor(provider, store).sync(build_domain_query(domains, query))
        save_settings(current.config_dir, last_sync=datetime.now(timezone.utc).isoformat())
    except ValueError as error:
        raise click.ClickException(str(error)) from error
    except Exception as error:
        raise click.ClickException(str(error)) from error
    finally:
        store.close()
    click.echo(f"Synchronized {count} email message(s).")


@sync.command("files")
@click.argument("path", required=False, type=click.Path(exists=True, path_type=Path))
@click.option("--ext", "-e", "extensions", multiple=True, help="File extensions to include (e.g. .md, .txt). Repeatable.")
def sync_files(path: Path | None, extensions: tuple[str, ...]) -> None:
    """Scan and index local markdown and text files."""
    if path is None:
        if _is_interactive():
            entered = click.prompt("Enter directory or file path to sync", default=".", show_default=True)
            path = Path(entered).expanduser()
        else:
            path = Path(".")

    current = _config()
    store = _store(current)
    try:
        ext_list = list(extensions) if extensions else None
        provider = LocalFileProvider(path, allowed_extensions=ext_list)
        count = FileIngestor(provider, store).sync()
        save_settings(current.config_dir, last_sync=datetime.now(timezone.utc).isoformat())
    except Exception as error:
        raise click.ClickException(str(error)) from error
    finally:
        store.close()
    click.echo(f"Synchronized {count} file(s) from {path}.")


@sync.command("web")
@click.option("--url", "urls", multiple=True, required=True, help="URL to fetch and index. Repeatable.")
@click.option("--domain", "domains", multiple=True, required=True, help="Allowed domain (subdomains included). Repeatable.")
@click.option("--timeout", default=30.0, type=float, show_default=True, help="Per-request timeout in seconds.")
def sync_web(urls: tuple[str, ...], domains: tuple[str, ...], timeout: float) -> None:
    """Fetch, normalize, and index web pages from allowed domains."""
    current = _config()
    store = _store(current)
    try:
        provider = HttpWebProvider(domains, timeout=timeout)
        count = WebIngestor(provider, store).sync(urls)
        save_settings(current.config_dir, last_sync=datetime.now(timezone.utc).isoformat())
    except ValueError as error:
        raise click.ClickException(str(error)) from error
    except Exception as error:
        raise click.ClickException(str(error)) from error
    finally:
        store.close()
    for skipped_url in provider.skipped:
        click.echo(f"Skipped (outside allowed domains): {skipped_url}")
    click.echo(f"Synchronized {count} web page(s).")


@sync.command("file", hidden=True)
@click.argument("path", required=False, type=click.Path(exists=True, path_type=Path))
@click.option("--ext", "-e", "extensions", multiple=True, help="File extensions to include (e.g. .md, .txt). Repeatable.")
def sync_file(path: Path | None, extensions: tuple[str, ...]) -> None:
    """Scan and index local markdown and text files."""
    sync_files.callback(path, extensions)


@main.command()
@click.option("--domain", "domains", multiple=True, help="Override domain filter for this update.")
@click.option("--query", default=None, help="Optional Gmail query (e.g. newer_than:7d).")
def update(domains: tuple[str, ...], query: str | None) -> None:
    """Update the context folder with latest data to keep it up to date."""
    current = _config()
    store = _store(current)
    click.echo(f"Updating context folder: {current.data_dir}")
    active_domains = domains if domains else current.saved_domains
    if active_domains:
        click.echo(f"Filtering by domain(s): {', '.join(active_domains)}")
    try:
        provider = GmailProvider(current.gmail_credentials_path, current.gmail_token_path)
        click.echo("Fetching and updating context data...")
        count = EmailIngestor(provider, store).sync(build_domain_query(active_domains, query))
        total_items = store.count()
        save_settings(current.config_dir, last_sync=datetime.now(timezone.utc).isoformat())
        click.echo(f"Updated {count} message(s).")
        click.echo(f"Context folder is up to date. Total items in folder: {total_items}")
    except Exception as error:
        raise click.ClickException(str(error)) from error
    finally:
        store.close()


@main.command("link")
def link() -> None:
    """Generate connection link and config for AI clients (Cursor, Claude, Cline)."""
    _display_mcp_links(_config())


@main.command("mcp-link")
def mcp_link() -> None:
    """Generate connection link and config for AI clients (Cursor, Claude, Cline)."""
    _display_mcp_links(_config())


@main.command()
def setup() -> None:
    """Interactive setup wizard for Self Context."""
    click.echo("=== Self Context Setup Wizard ===\n")
    current = _config()
    chosen_dir = click.prompt(
        "1. Select directory where scraped data will live",
        default=str(current.data_dir),
        show_default=True,
    )
    data_dir = Path(chosen_dir).expanduser()
    save_settings(current.config_dir, data_dir=data_dir)
    current = _config(data_dir=data_dir)
    store = _store(current)
    store.close()
    click.echo(f"   [OK] Data directory set to {current.data_dir}\n")

    if not current.gmail_credentials_path or not current.gmail_credentials_path.exists():
        creds_input = click.prompt(
            "2. Enter path to Google OAuth client secret JSON (or press Enter to skip)",
            default="",
            show_default=False,
        ).strip()
        if creds_input:
            creds_path = Path(creds_input).expanduser()
            if creds_path.exists():
                save_settings(current.config_dir, gmail_credentials_path=creds_path)
                current = _config(data_dir=data_dir)
                click.echo("   [OK] Credentials configured.\n")
            else:
                click.echo(f"   [Warning] File not found: {creds_path}. Skipping auth.\n")
    else:
        click.echo(f"   [OK] Credentials already configured: {current.gmail_credentials_path}\n")

    default_dom = ", ".join(current.saved_domains) if current.saved_domains else ""
    domain_input = click.prompt(
        "3. Enter domain to scrape/filter emails (e.g. company.com), or press Enter for all",
        default=default_dom,
        show_default=bool(default_dom),
    ).strip()
    if domain_input:
        doms = tuple(d.strip() for d in re.split(r"[, ]+", domain_input) if d.strip())
        save_settings(current.config_dir, domains=doms)
        current = _config(data_dir=data_dir)
        click.echo(f"   [OK] Saved domain filter: {', '.join(doms)}\n")

    click.echo("4. AI MCP Connection Links:")
    _display_mcp_links(current)
    click.echo("Setup complete! You can now run 'self-context update' to keep your folder up to date.")


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


@main.command("delete")
@click.argument("item_id")
def delete_item(item_id: str) -> None:
    """Delete one indexed context item by ID."""
    store = _store(_config())
    try:
        deleted = store.delete(item_id)
    finally:
        store.close()
    if not deleted:
        raise click.ClickException(f"Context item not found: {item_id}")
    click.echo(f"Deleted context item: {item_id}")


@main.command("list")
@click.option("--source", default=None)
@click.option("--type", "item_type", default=None)
@click.option("--limit", default=20, type=int)
def list_items(source: str | None, item_type: str | None, limit: int) -> None:
    """List recently indexed context items."""
    store = _store(_config())
    try:
        items = RetrievalService(store).list_items(source=source, type=item_type, limit=limit)
        for item in items:
            click.echo(f"{item.id}\t{item.title}")
    finally:
        store.close()


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
@click.option("--link", is_flag=True, default=False, help="Show AI connection link and configuration instead of starting server.")
@click.option("--print-config", is_flag=True, default=False, help="Print the MCP client configuration JSON and exit.")
@click.option("--install", "client", type=click.Choice(sorted(_MCP_CLIENT_CONFIG_PATHS)), default=None,
              help="Write the MCP server entry into the given client's config file and exit.")
def mcp(link: bool, print_config: bool, client: str | None) -> None:
    """Start the local MCP server over stdio or show connection link."""
    current = _config()
    if client:
        config_path = _install_mcp_config(client)
        click.echo(f"Installed self-context MCP server into {client} config: {config_path}")
        return
    if print_config:
        _, json_config = _generate_mcp_links(_get_mcp_command())
        click.echo(json_config)
        return
    if link:
        _display_mcp_links(current)
        return
    from .mcp.server import run_server
    run_server(current)


if __name__ == "__main__":
    main(sys.argv[1:])