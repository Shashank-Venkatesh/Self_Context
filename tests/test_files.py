from datetime import datetime, timezone
from pathlib import Path

from click.testing import CliRunner

from self_context.cli import main
from self_context.sources.files import FileIngestor, LocalFileProvider
from self_context.sources.files.models import FileDocument
from self_context.sources.files.normalization import normalize_file_document


def test_file_document_dataclass():
    now = datetime.now(timezone.utc)
    doc = FileDocument(
        path="/tmp/test.md",
        relative_path="test.md",
        file_type=".md",
        title="Test",
        content="Sample content",
        size=14,
        mtime=now,
        checksum="hash123",
    )
    assert doc.path == "/tmp/test.md"
    assert doc.relative_path == "test.md"
    assert doc.file_type == ".md"
    assert doc.title == "Test"
    assert doc.content == "Sample content"
    assert doc.size == 14
    assert doc.mtime == now
    assert doc.checksum == "hash123"
    assert doc.metadata == {}


def test_local_file_provider_scanning_and_filtering(tmp_path):
    # Setup test directory structure
    (tmp_path / "note1.md").write_text("# Note 1\nContent 1", encoding="utf-8")
    (tmp_path / "note2.txt").write_text("Plain text content", encoding="utf-8")
    (tmp_path / "doc.rst").write_text("RST Document", encoding="utf-8")
    (tmp_path / "org.org").write_text("* Org Header", encoding="utf-8")
    (tmp_path / "ignored.pdf").write_bytes(b"%PDF-1.4 ignored")
    (tmp_path / ".hidden_file.md").write_text("Hidden file", encoding="utf-8")

    sub_dir = tmp_path / "sub"
    sub_dir.mkdir()
    (sub_dir / "nested.markdown").write_text("Nested markdown", encoding="utf-8")

    ignored_dir = tmp_path / "node_modules"
    ignored_dir.mkdir()
    (ignored_dir / "package_note.md").write_text("Ignored note", encoding="utf-8")

    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "COMMIT_EDITMSG.txt").write_text("Commit msg", encoding="utf-8")

    provider = LocalFileProvider(tmp_path)
    docs = list(provider.scan_files())
    rel_paths = {doc.relative_path for doc in docs}

    assert "note1.md" in rel_paths
    assert "note2.txt" in rel_paths
    assert "doc.rst" in rel_paths
    assert "org.org" in rel_paths
    assert str(Path("sub") / "nested.markdown") in rel_paths
    assert "ignored.pdf" not in rel_paths
    assert ".hidden_file.md" not in rel_paths
    assert str(Path("node_modules") / "package_note.md") not in rel_paths
    assert str(Path(".git") / "COMMIT_EDITMSG.txt") not in rel_paths


def test_local_file_provider_single_file(tmp_path):
    single_file = tmp_path / "single.md"
    single_file.write_text("# Single File\nContent", encoding="utf-8")

    provider = LocalFileProvider(single_file)
    docs = list(provider.scan_files())
    assert len(docs) == 1
    assert docs[0].title == "single"
    assert docs[0].content == "# Single File\nContent"


def test_local_file_provider_custom_extensions(tmp_path):
    (tmp_path / "code.py").write_text("print('hello')", encoding="utf-8")
    (tmp_path / "note.md").write_text("Markdown note", encoding="utf-8")

    provider = LocalFileProvider(tmp_path, allowed_extensions=[".py"])
    docs = list(provider.scan_files())
    assert len(docs) == 1
    assert docs[0].relative_path == "code.py"


def test_normalization_frontmatter_extraction():
    content = """---
title: YAML Frontmatter Title
tags: [python, test]
author: Alice
---
# Heading Title

Body text here.
"""
    doc = FileDocument(
        path="/tmp/test.md",
        relative_path="test.md",
        file_type=".md",
        title="test",
        content=content,
        size=len(content),
        mtime=datetime.now(timezone.utc),
        checksum="abc",
    )

    normalized = normalize_file_document(doc)
    assert normalized.title == "YAML Frontmatter Title"
    assert normalized.metadata["tags"] == ["python", "test"]
    assert normalized.metadata["author"] == "Alice"
    assert "# Heading Title" in normalized.content
    assert "---" not in normalized.content


def test_normalization_h1_fallback():
    content = """# First H1 Title

Some details in document.
"""
    doc = FileDocument(
        path="/tmp/h1_test.md",
        relative_path="h1_test.md",
        file_type=".md",
        title="h1_test",
        content=content,
        size=len(content),
        mtime=datetime.now(timezone.utc),
        checksum="def",
    )

    normalized = normalize_file_document(doc)
    assert normalized.title == "First H1 Title"


def test_normalization_basename_fallback():
    content = "Just plain text without headings or frontmatter."
    doc = FileDocument(
        path="/tmp/plain_note.txt",
        relative_path="plain_note.txt",
        file_type=".txt",
        title="plain_note",
        content=content,
        size=len(content),
        mtime=datetime.now(timezone.utc),
        checksum="ghi",
    )

    normalized = normalize_file_document(doc)
    assert normalized.title == "plain_note.txt"


def test_file_ingestor(tmp_path, store):
    (tmp_path / "doc1.md").write_text("---\ntitle: Doc 1\n---\nHello World", encoding="utf-8")
    (tmp_path / "doc2.txt").write_text("# Doc 2 Header\nText content", encoding="utf-8")

    provider = LocalFileProvider(tmp_path)
    ingestor = FileIngestor(provider, store)

    count = ingestor.sync()
    assert count == 2
    assert store.count() == 2

    item1 = store.get_by_source("file", "doc1.md")
    assert item1 is not None
    assert item1.title == "Doc 1"
    assert item1.content == "Hello World"
    assert item1.source == "file"
    assert item1.type == "file"

    item2 = store.get_by_source("file", "doc2.txt")
    assert item2 is not None
    assert item2.title == "Doc 2 Header"

    # Repeat sync should update idempotently
    assert ingestor.sync() == 2
    assert store.count() == 2


def test_cli_sync_files_command(tmp_path, monkeypatch):
    config_dir = tmp_path / "config"
    data_dir = tmp_path / "data"
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()

    (docs_dir / "readme.md").write_text("# Project Readme\nWelcome!", encoding="utf-8")
    (docs_dir / "notes.txt").write_text("General notes", encoding="utf-8")

    monkeypatch.setenv("XDG_CONFIG_HOME", str(config_dir))
    monkeypatch.setenv("XDG_DATA_HOME", str(data_dir))

    runner = CliRunner()
    runner.invoke(main, ["init", "--data-dir", str(data_dir)])

    result = runner.invoke(main, ["sync", "files", str(docs_dir)])
    assert result.exit_code == 0
    assert "Synchronized 2 file(s)" in result.output

    # Check that item is retrievable via search
    search_result = runner.invoke(main, ["search", "Readme"])
    assert search_result.exit_code == 0
    assert "Project Readme" in search_result.output
