from click.testing import CliRunner

from self_context.cli import main


def test_sync_email_help_describes_domain_filter():
    result = CliRunner().invoke(main, ["sync", "email", "--help"])
    assert result.exit_code == 0
    assert "Repeatable" in result.output
    assert "domain" in result.output