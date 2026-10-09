"""Normalizer for local file documents (frontmatter, title, and metadata extraction)."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from .models import FileDocument


def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML frontmatter from document content.

    Returns a tuple of (metadata_dict, body_content).
    """
    if not content.startswith("---"):
        return {}, content

    lines = content.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, content

    end_index = -1
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            end_index = i
            break

    if end_index == -1:
        return {}, content

    frontmatter_text = "".join(lines[1:end_index])
    body_text = "".join(lines[end_index + 1:])

    metadata = _parse_yaml_simple(frontmatter_text)
    return metadata, body_text


def _parse_yaml_simple(text: str) -> dict[str, Any]:
    """Parse simple YAML text into a dict."""
    try:
        import yaml
        result = yaml.safe_load(text)
        if isinstance(result, dict):
            return result
    except Exception:
        pass

    data: dict[str, Any] = {}
    current_list_key = None
    for line in text.splitlines():
        line_str = line.strip()
        if not line_str or line_str.startswith("#"):
            continue

        if line_str.startswith("- ") and current_list_key:
            val = line_str[2:].strip().strip("\"'")
            if isinstance(data.get(current_list_key), list):
                data[current_list_key].append(val)
            else:
                data[current_list_key] = [val]
            continue

        if ":" in line_str:
            key, val = line_str.split(":", 1)
            key = key.strip()
            val = val.strip()
            current_list_key = None

            if not val:
                data[key] = []
                current_list_key = key
            elif val.startswith("[") and val.endswith("]"):
                items = [item.strip().strip("\"'") for item in val[1:-1].split(",") if item.strip()]
                data[key] = items
            else:
                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                data[key] = val

    return data


def normalize_file_document(file_doc: FileDocument) -> FileDocument:
    """Extract frontmatter title/metadata or first H1 heading from FileDocument."""
    metadata, body_content = parse_frontmatter(file_doc.content)

    title = None
    if "title" in metadata and metadata["title"]:
        title = str(metadata["title"]).strip()

    if not title:
        for line in body_content.splitlines():
            line_str = line.strip()
            if line_str.startswith("# "):
                title = line_str[2:].strip()
                break
            elif line_str.startswith("#") and not line_str.startswith("##"):
                title = line_str.lstrip("#").strip()
                break

    if not title:
        title = Path(file_doc.path).name or Path(file_doc.relative_path).name or file_doc.title or "Untitled"

    if "tags" in metadata:
        tags = metadata["tags"]
        if isinstance(tags, str):
            metadata["tags"] = [t.strip() for t in tags.split(",") if t.strip()]
        elif isinstance(tags, list):
            metadata["tags"] = [str(t).strip() for t in tags if str(t).strip()]

    merged_metadata = dict(metadata)
    merged_metadata.update({
        "path": file_doc.path,
        "relative_path": file_doc.relative_path,
        "file_type": file_doc.file_type,
        "size": file_doc.size,
        "mtime": file_doc.mtime.isoformat() if isinstance(file_doc.mtime, datetime) else str(file_doc.mtime),
        "checksum": file_doc.checksum,
    })

    return FileDocument(
        path=file_doc.path,
        relative_path=file_doc.relative_path,
        file_type=file_doc.file_type,
        title=title,
        content=body_content,
        size=file_doc.size,
        mtime=file_doc.mtime,
        checksum=file_doc.checksum,
        metadata=merged_metadata,
    )
