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

## 5. Initialize local storage

Create the local configuration, data, and cache directories:

```bash
.venv/bin/self-context init
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

## 6. Optional: use different local directories

Set these variables before running the CLI if you want to keep the data somewhere else:

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

Use this configuration and replace the command path with the path on your machine:

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

The server provides:

- `search_context`
- `get_context_item`
- `search_emails`
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
