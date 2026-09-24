from datetime import datetime, timezone

from self_context.core.models import ContextItem
from self_context.core.retrieval import RetrievalService
from self_context.mcp.server import create_server


def test_mcp_context_tools_search_and_get(store):
    now = datetime.now(timezone.utc)
    store.add(ContextItem("email:1", "email", "1", "email", "Project meeting",
                          "Discussed machine learning", {}, now, now, now))
    server = create_server(RetrievalService(store))
    tools = server._tool_manager._tools

    search_result = tools["search_context"].fn("machine")
    email_result = tools["search_emails"].fn("meeting")
    item_result = tools["get_context_item"].fn("email:1")

    assert search_result[0]["id"] == "email:1"
    assert email_result[0]["source"] == "email"
    assert item_result["title"] == "Project meeting"