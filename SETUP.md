# Self Context Setup

This guide installs Self Context and gets the local CLI ready to use.

## 1. Requirements

You need:

- Linux
- Python 3.11 or newer
- A terminal
- A Google account only if you want to import Gmail

Check Python:

```bash
python3 --version
```

## 2. Open the project folder

Replace the path below if the project is stored somewhere else:

```bash
cd /home/scatterzz/Documents/Projects/Self_Context
```

## 3. Create a virtual environment

A virtual environment keeps this project's packages separate from other Python projects.

```bash
python3 -m venv .venv
```

## 4. Install Self Context

Install the application and its development tools:

```bash
.venv/bin/python -m pip install -e '.[dev]'
```

Check that the command is available:

```bash
.venv/bin/self-context --version
```

## 5. Initialize local storage (or run setup wizard)

You can run the interactive setup wizard which guides you through directory selection, authentication, domain filters, and MCP link generation:

```bash
.venv/bin/self-context setup
```

Or initialize manually:

```bash
.venv/bin/self-context init
```

To store your scraped data in a custom folder, pass `--data-dir`:

```bash
.venv/bin/self-context init --data-dir /path/to/my-data
```

Check the installation:

```bash
.venv/bin/self-context config
.venv/bin/self-context status
```

You should see:

- A configuration directory
- A data directory
- A SQLite database path
- `gmail_credentials: not configured` unless Gmail has been set up
- `items: 0` on a new installation

By default, files are stored here:

- Configuration and Gmail token: `~/.config/self-context/`
- Database: `~/.local/share/self-context/context.sqlite3`
- Cache: `~/.cache/self-context/`

## 6. Optional: select or change the data directory

Set the data directory at any time without environment variables:

```bash
.venv/bin/self-context config --data-dir /path/to/my-data
```

Or set standard XDG variables before running the CLI:

```bash
export XDG_CONFIG_HOME="$HOME/.config"
export XDG_DATA_HOME="$HOME/.local/share"
export XDG_CACHE_HOME="$HOME/.cache"
```

Self Context creates a `self-context` directory inside each location.

## 7. Optional: connect Gmail

Skip this section if you only want to use the local database or run tests.

### Create Google credentials

1. Open the Google Cloud Console.
2. Create or select a project.
3. Enable the Gmail API.
4. Create an OAuth client for a desktop application.
5. Download the client JSON file.
6. Store it outside this repository.

Set the path to the downloaded file:

```bash
export SELF_CONTEXT_GMAIL_CREDENTIALS="/absolute/path/to/client_secret.json"
```

Confirm that Self Context can see the configuration:

```bash
.venv/bin/self-context config
```

The output should include:

```text
gmail_credentials: configured
```

### Sign in

Run:

```bash
.venv/bin/self-context auth gmail
```

A browser window opens. Sign in and approve read-only Gmail access.

The token is stored locally at:

```text
~/.config/self-context/gmail-token.json
```

Do not commit the client JSON or token to source control.

## 8. Import email

Start with a small, recent query:

```bash
.venv/bin/self-context sync email --query 'newer_than:7d'
```

To import only messages involving specific domains:

```bash
.venv/bin/self-context sync email \
  --domain company.com \
  --domain partner.org \
  --query 'newer_than:30d'
```

Check how many items were imported:

```bash
.venv/bin/self-context status
```

Run the same sync again when needed. Existing Gmail messages are updated instead of duplicated.

### Import web pages

Self Context can also fetch and index web pages, restricted to an explicit domain allowlist:

```bash
.venv/bin/self-context sync web \
  --url https://docs.example.com/guide \
  --url https://blog.example.com/post \
  --domain example.com
```

Each `--domain` allows that exact domain and its subdomains; repeat `--url` and `--domain` to add more. URLs outside the allowlist are skipped and reported. Use `--timeout N` to change the per-request timeout in seconds (default 30). Re-running the same sync updates existing pages instead of duplicating them, because items are keyed by canonical URL.

### Keep the folder up to date

To easily refresh your data folder at any time, run:

```bash
.venv/bin/self-context update
```

This automatically applies your saved domain filters, fetches recent emails, and keeps the local SQLite database up to date.

## 9. Search and view imported context

Search by keyword:

```bash
.venv/bin/self-context search "project meeting"
```

Search only email items:

```bash
.venv/bin/self-context search --source email "project meeting"
```

Get one item by its ID:

```bash
.venv/bin/self-context get email:<gmail-message-id>
```

The search output shows the item ID and title. Use the ID from that output with the `get` command.

## 10. Optional: connect an MCP client

Self Context can provide local context to an MCP-compatible AI client.

### Generate AI Connection Link & Configuration

You can automatically generate your machine's exact connection link and configuration directly from the CLI:

```bash
.venv/bin/self-context link
```
*(or `.venv/bin/self-context mcp --link`)*

This prints:
1. The **Cursor One-Click Deep Link** with the correct paths encoded.
2. The ready-to-copy JSON configuration for Claude Desktop and Cline:

```json
{
  "mcpServers": {
    "self-context": {
      "command": "/absolute/path/to/Self_Context/.venv/bin/self-context",
      "args": ["mcp"]
    }
  }
}
```


### Print or install the client configuration

To print just the ready-to-copy JSON configuration without the deep link:

```bash
.venv/bin/self-context mcp --print-config
```

To merge the `self-context` server entry directly into a supported client's `mcpServers` configuration file:

```bash
.venv/bin/self-context mcp --install claude
.venv/bin/self-context mcp --install cline
.venv/bin/self-context mcp --install cursor
```

The install command preserves any existing entries in the client's config file and only adds or updates the `self-context` server. It writes to:

- Claude Desktop: `~/.config/Claude/claude_desktop_config.json`
- Cline: `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
- Cursor: `~/.cursor/mcp.json`

#### One-Click Install for Cursor
You can also connect to Cursor with a single click using Cursor's MCP deep link:
```text
cursor://anysphere.cursor-deeplink/mcp/install?name=self-context&config=eyJjb21tYW5kIjogIi9ob21lL3NjYXR0ZXJ6ei9Eb2N1bWVudHMvUHJvamVjdHMvU2VsZl9Db250ZXh0Ly52ZW52L2Jpbi9zZWxmLWNvbnRleHQiLCAiYXJncyI6IFsibWNwIl19
```
*(Update the Base64-encoded config if running from a different directory path.)*

The server provides:

- `search_context`
- `get_context_item`
- `search_emails`
- `search_web`
- `context://item/<id>`

The MCP server uses the same local database as the CLI and communicates over standard input/output.

## 11. Run the checks

Run the automated tests:

```bash
.venv/bin/pytest -q
```

Run the code-quality check:

```bash
.venv/bin/ruff check src tests
```

Both commands should finish successfully.

## 12. Common problems

### `python3: command not found`

Install Python 3.11 or newer using your Linux distribution's package manager, then repeat the installation steps.

### `.venv/bin/self-context: No such file or directory`

The virtual environment or package installation is incomplete. Run:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -e '.[dev]'
```

### `Gmail OAuth is not configured`

Set `SELF_CONTEXT_GMAIL_CREDENTIALS` to the full path of the Google OAuth client JSON file, then run `auth gmail` again.

### The browser sign-in does not start

Run the command from a terminal with a graphical browser available. If you are using a remote or headless machine, complete the OAuth flow in an environment that supports the installed-app browser flow.

### No email is imported

Check the Gmail query, date range, and domain filters. Try a small query without a domain filter:

```bash
.venv/bin/self-context sync email --query 'newer_than:1d'
```

### Reset local data

Only do this if you want to delete the local index and start again:

```bash
rm -rf "$HOME/.local/share/self-context"
```

This deletes the local SQLite database. The Gmail OAuth token remains in the configuration directory unless you remove it separately.
