from resources.doc_loader import DocLoader


def test_scan_docs(resource_dir):
    loader = DocLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    assert len(loader.docs) == 4


def test_search_by_topic(resource_dir):
    loader = DocLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("开发经验")
    assert len(results) >= 1
    assert any("开发经验" in r["title"] for r in results)


def test_search_filter_by_type(resource_dir):
    loader = DocLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("模板", doc_type="template")
    assert all(r["type"] == "template" for r in results)


def test_search_returns_fields(resource_dir):
    loader = DocLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("开发经验")
    assert len(results) >= 1
    r = results[0]
    for field in ("id", "title", "path", "type", "language", "tags", "summary", "content", "size"):
        assert field in r


def test_search_no_match(resource_dir):
    loader = DocLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("不存在的主题xyz")
    assert results == []


def test_search_respects_limit(resource_dir):
    loader = DocLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("的", limit=1)
    assert len(results) == 1


def test_search_content_match(resource_dir):
    loader = DocLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("编码规范")
    assert len(results) >= 1
    assert any("编码规范" in r["content"] for r in results)


def test_search_ordering_by_relevance(resource_dir):
    """Verify that a title match (score 3) ranks higher than a summary/content-only match (score 1+1)."""
    docs_dir = resource_dir / "i18n" / "zh" / "documents" / "Methodology and Principles"
    (docs_dir / "编码规范指南.md").write_text(
        "# 编码规范指南\n\n详细的编码规范说明。",
        encoding="utf-8",
    )
    loader = DocLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("编码规范")
    assert len(results) >= 2
    assert "编码规范指南" in results[0]["title"]
