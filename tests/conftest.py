from pathlib import Path

import pytest

from self_context.core.storage import ContextStore


@pytest.fixture
def store(tmp_path: Path) -> ContextStore:
    value = ContextStore(tmp_path / "context.sqlite3")
    yield value
    value.close()