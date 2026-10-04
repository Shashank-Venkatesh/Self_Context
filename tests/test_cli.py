import json
from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from self_context.cli import main


def test_sync_email_help_describes_domain_filter():
    result = CliRunner().invoke(main, ["sync", "email", "--help"])
    assert result.exit_code == 0
    assert "Repeatable" in result.output
    assert "domain" in result.output


def test_init_with_custom_data_dir(tmp_path, monkeypatch):
    config_dir = tmp_path / "config"
    data_dir = tmp_path / "custom_data"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))
    monkeypatch.delenv("XDG_DATA_HOME", raising=False)

    runner = CliRunner()
    result = runner.invoke(main, ["init", "--data-dir", str(data_dir)])
    assert result.exit_code == 0
    assert f"Initialized Self Context in {data_dir}" in result.output
    assert (data_dir / "context.sqlite3").exists()

    config_result = runner.invoke(main, ["config"])
    assert config_result.exit_code == 0
    assert str(data_dir) in config_result.output


def test_config_set_data_dir(tmp_path, monkeypatch):
    config_dir = tmp_path / "config"
    new_dir = tmp_path / "another_data"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))
    monkeypatch.delenv("XDG_DATA_HOME", raising=False)

    runner = CliRunner()
    result = runner.invoke(main, ["config", "--data-dir", str(new_dir)])
    assert result.exit_code == 0
    assert f"Updated data directory to: {new_dir}" in result.output


def test_mcp_link_and_options():
    runner = CliRunner()

    result_link = runner.invoke(main, ["link"])
    assert result_link.exit_code == 0
    assert "cursor://anysphere.cursor-deeplink/mcp/install?name=self-context&config=" in result_link.output
    assert '"mcpServers"' in result_link.output

    result_mcp_link = runner.invoke(main, ["mcp-link"])
    assert result_mcp_link.exit_code == 0
    assert "cursor://" in result_mcp_link.output

    result_mcp_flag = runner.invoke(main, ["mcp", "--link"])
    assert result_mcp_flag.exit_code == 0
    assert "cursor://" in result_mcp_flag.output


def test_update_command(tmp_path, monkeypatch):
    config_dir = tmp_path / "config"
    data_dir = tmp_path / "data"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))
    monkeypatch.setenv("XDG_DATA_HOME", str(data_dir))

    runner = CliRunner()
    runner.invoke(main, ["init", "--data-dir", str(data_dir)])

    with patch("self_context.cli.GmailProvider") as mock_provider_cls, \
         patch("self_context.cli.EmailIngestor") as mock_ingestor_cls:
        mock_provider = MagicMock()
        mock_provider_cls.return_value = mock_provider
        mock_ingestor = MagicMock()
        mock_ingestor.sync.return_value = 5
        mock_ingestor_cls.return_value = mock_ingestor

        result = runner.invoke(main, ["update", "--domain", "example.com"])
        assert result.exit_code == 0
        assert "Updating context folder:" in result.output
        assert "Updated 5 message(s)" in result.output
        assert "Context folder is up to date" in result.output


def test_sync_email_domain_prompt(tmp_path, monkeypatch):
    config_dir = tmp_path / "config"
    data_dir = tmp_path / "data"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))
    monkeypatch.setenv("XDG_DATA_HOME", str(data_dir))

    runner = CliRunner()
    runner.invoke(main, ["init", "--data-dir", str(data_dir)])

    with patch("self_context.cli.GmailProvider") as mock_provider_cls, \
         patch("self_context.cli.EmailIngestor") as mock_ingestor_cls:
        mock_provider = MagicMock()
        mock_provider_cls.return_value = mock_provider
        mock_ingestor = MagicMock()
        mock_ingestor.sync.return_value = 3
        mock_ingestor_cls.return_value = mock_ingestor

        # Simulate user typing domain at prompt
        with patch("sys.stdin.isatty", return_value=True):
            result = runner.invoke(main, ["sync", "email"], input="partner.com\n")
            assert result.exit_code == 0
            assert "Synchronized 3 email message(s)" in result.output

            # Check that domain was saved in config
            config_result = runner.invoke(main, ["config"])
            assert "partner.com" in config_result.output


def test_setup_wizard(tmp_path, monkeypatch):
    config_dir = tmp_path / "config"
    target_data_dir = tmp_path / "wizard_data"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))
    monkeypatch.delenv("XDG_DATA_HOME", raising=False)

    runner = CliRunner()
    # Step 1: data dir, Step 2: credentials (skip by enter), Step 3: domain filter
    user_inputs = f"{target_data_dir}\n\nexample.org\n"
    result = runner.invoke(main, ["setup"], input=user_inputs)
    assert result.exit_code == 0
    assert "Self Context Setup Wizard" in result.output
    assert f"Data directory set to {target_data_dir}" in result.output
    assert "Saved domain filter: example.org" in result.output
    assert "cursor://" in result.output

def test_sync_web_with_mocked_provider(tmp_path, monkeypatch):
    config_dir = tmp_path / "config"
    data_dir = tmp_path / "data"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))
    monkeypatch.setenv("XDG_DATA_HOME", str(data_dir))

    runner = CliRunner()
    runner.invoke(main, ["init", "--data-dir", str(data_dir)])

    with patch("self_context.cli.HttpWebProvider") as mock_provider_cls, \
         patch("self_context.cli.WebIngestor") as mock_ingestor_cls:
        mock_provider = MagicMock()
        mock_provider.skipped = ["https://evil.com/"]
        mock_provider_cls.return_value = mock_provider
        mock_ingestor = MagicMock()
        mock_ingestor.sync.return_value = 2
        mock_ingestor_cls.return_value = mock_ingestor

        result = runner.invoke(main, ["sync", "web",
                                      "--url", "https://example.com/a",
                                      "--url", "https://example.com/b",
                                      "--domain", "example.com",
                                      "--timeout", "5"])
        assert result.exit_code == 0
        mock_provider_cls.assert_called_once_with(("example.com",), timeout=5.0)
        mock_ingestor.sync.assert_called_once_with(("https://example.com/a", "https://example.com/b"))
        assert "Skipped (outside allowed domains): https://evil.com/" in result.output
        assert "Synchronized 2 web page(s)." in result.output


def test_sync_web_requires_url_and_domain():
    result = CliRunner().invoke(main, ["sync", "web"])
    assert result.exit_code != 0
    assert "--url" in result.output


def test_sync_web_invalid_domain_fails_cleanly(tmp_path, monkeypatch):
    config_dir = tmp_path / "config"
    data_dir = tmp_path / "data"
    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))
    monkeypatch.setenv("XDG_DATA_HOME", str(data_dir))

    runner = CliRunner()
    runner.invoke(main, ["init", "--data-dir", str(data_dir)])

    result = runner.invoke(main, ["sync", "web", "--url", "https://example.com/",
                                  "--domain", "not a domain"])
    assert result.exit_code != 0
    assert "Invalid domain" in result.output


def test_mcp_print_config_outputs_valid_json():
    result = CliRunner().invoke(main, ["mcp", "--print-config"])
    assert result.exit_code == 0
    config = json.loads(result.output)
    server = config["mcpServers"]["self-context"]
    assert server["args"] == ["mcp"]
    assert server["command"]


def test_mcp_install_writes_client_config(tmp_path, monkeypatch):
    import self_context.cli as cli_module
    config_path = tmp_path / "cursor" / "mcp.json"
    monkeypatch.setitem(cli_module._MCP_CLIENT_CONFIG_PATHS, "cursor", config_path)

    result = CliRunner().invoke(main, ["mcp", "--install", "cursor"])
    assert result.exit_code == 0
    assert "Installed self-context MCP server into cursor config" in result.output

    written = json.loads(config_path.read_text(encoding="utf-8"))
    assert written["mcpServers"]["self-context"]["args"] == ["mcp"]

    # Existing entries are preserved on re-install.
    config_path.write_text(json.dumps({"mcpServers": {"other": {"command": "other", "args": []}}}),
                           encoding="utf-8")
    result = CliRunner().invoke(main, ["mcp", "--install", "cursor"])
    assert result.exit_code == 0
    written = json.loads(config_path.read_text(encoding="utf-8"))
    assert "other" in written["mcpServers"]
    assert "self-context" in written["mcpServers"]
