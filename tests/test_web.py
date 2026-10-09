import pytest

from self_context.core.retrieval import RetrievalService
from self_context.sources.web.ingestion import WebIngestor
from self_context.sources.web.normalization import canonicalize_url, extract_text, normalize_web_page
from self_context.sources.web.providers import HttpWebProvider, is_allowed, normalize_domain


def test_normalize_domain_strips_scheme_port_and_path():
    assert normalize_domain("https://Example.COM:8443/some/path") == "example.com"
    assert normalize_domain("  Docs.Example.com ") == "docs.example.com"


def test_normalize_domain_rejects_invalid():
    for bad in ("not a domain", "example", "-bad.com", "example..com", ""):
        with pytest.raises(ValueError, match="Invalid domain"):
            normalize_domain(bad)


def test_is_allowed_exact_and_subdomain():
    domains = ["example.com"]
    assert is_allowed("https://example.com/page", domains)
    assert is_allowed("https://docs.example.com/page", domains)
    assert is_allowed("http://deep.sub.example.com/", domains)


def test_is_allowed_rejects_evil_suffix_and_other_hosts():
    domains = ["example.com"]
    assert not is_allowed("https://example.com.evil.com/", domains)
    assert not is_allowed("https://notexample.com/", domains)
    assert not is_allowed("https://example.com.attacker.net/path", domains)
    assert not is_allowed("not-a-url", domains)


def test_is_allowed_is_case_insensitive():
    assert is_allowed("HTTPS://EXAMPLE.COM/Page", ["example.com"])


def test_canonicalize_url_is_idempotent():
    url = canonicalize_url("HTTPS://Example.COM:443/Path?b=2#frag")
    assert url == "https://example.com/Path?b=2"
    assert canonicalize_url(url) == url
    assert canonicalize_url("http://example.com:80/a") == "http://example.com/a"
    assert canonicalize_url("https://example.com:8443/a") == "https://example.com:8443/a"
    assert canonicalize_url("https://example.com") == "https://example.com/"


def test_extract_text_strips_scripts_and_gets_title():
    html = (
        "<html><head><title>  My   Page </title>"
        "<style>body { color: red; }</style></head>"
        "<body><h1>Hello</h1><p>World <b>wide</b> web</p>"
        "<script>var x = 1;</script></body></html>"
    )
    text, title = extract_text(html)
    assert title == "My Page"
    assert "Hello" in text
    assert "World wide web" in text
    assert "var x" not in text
    assert "color: red" not in text


def test_normalize_web_page_falls_back_to_url_title():
    page = normalize_web_page({"url": "https://example.com/", "final_url": "https://example.com/",
                               "content_type": "text/html", "html": "<p>hi</p>"})
    assert page.title == "https://example.com/"
    assert page.text == "hi"
    assert page.canonical_url == "https://example.com/"


class FakeWebProvider:
    def __init__(self, pages):
        self.pages = pages

    def fetch_pages(self, urls):
        for url in urls:
            if url in self.pages:
                yield self.pages[url]


def page(url, html, final_url=None):
    return {"url": url, "final_url": final_url or url, "content_type": "text/html", "html": html}


def test_web_ingestor_stores_and_repeat_sync_is_idempotent(store):
    pages = {"https://example.com/a": page("https://example.com/a", "<title>A</title><p>alpha body</p>")}
    ingestor = WebIngestor(FakeWebProvider(pages), store)
    assert ingestor.sync(["https://example.com/a"]) == 1
    assert ingestor.sync(["https://example.com/a"]) == 1
    assert store.count() == 1
    item = store.get_by_source("web", "https://example.com/a")
    assert item.title == "A"
    assert item.content == "alpha body"
    assert item.id == "web:https://example.com/a"


def test_web_ingestor_canonicalizes_equivalent_urls_to_one_item(store):
    pages = {
        "https://example.com/a#top": page("https://example.com/a#top", "<p>one</p>"),
        "https://EXAMPLE.com:443/a": page("https://EXAMPLE.com:443/a", "<p>one</p>"),
    }
    ingestor = WebIngestor(FakeWebProvider(pages), store)
    assert ingestor.sync(list(pages)) == 2
    assert store.count() == 1


def test_web_ingestor_follows_final_url_for_canonical_id(store):
    pages = {"https://example.com/old": page("https://example.com/old", "<p>moved</p>",
                                             final_url="https://example.com/new")}
    ingestor = WebIngestor(FakeWebProvider(pages), store)
    assert ingestor.sync(["https://example.com/old"]) == 1
    assert store.get("web:https://example.com/new") is not None


def test_search_web_returns_only_web_items(store):
    pages = {"https://example.com/a": page("https://example.com/a", "<title>Doc</title><p>python tutorial</p>")}
    WebIngestor(FakeWebProvider(pages), store).sync(["https://example.com/a"])
    retrieval = RetrievalService(store)
    results = retrieval.search_web("python")
    assert len(results) == 1
    assert results[0].source == "web"
    assert retrieval.search_emails("python") == []


def test_http_provider_requires_domains():
    with pytest.raises(ValueError, match="At least one allowed domain"):
        HttpWebProvider([])


def test_http_provider_skips_disallowed_urls_without_network():
    provider = HttpWebProvider(["example.com"])
    assert provider.fetch_page("https://evil.com/") is None
    assert provider.fetch_page("https://example.com.evil.com/") is None
    assert provider.skipped == ["https://evil.com/", "https://example.com.evil.com/"]
    assert list(provider.fetch_pages(["https://evil.com/"])) == []
