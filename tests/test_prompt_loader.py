from resources.prompt_loader import PromptLoader


def test_scan_prompts(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh", "en"])
    loader.scan()
    assert len(loader.prompts) == 5  # 4 i18n + 1 prompt_docs


def test_scan_prompts_includes_prompt_docs(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"], include_prompt_docs=True)
    loader.scan()
    prompt_docs = [p for p in loader.prompts.values() if p["category"] == "prompt_docs"]
    assert len(prompt_docs) == 1
    assert "架构设计" in prompt_docs[0]["title"]


def test_scan_prompts_excludes_prompt_docs(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"], include_prompt_docs=False)
    loader.scan()
    prompt_docs = [p for p in loader.prompts.values() if p["category"] == "prompt_docs"]
    assert len(prompt_docs) == 0


def test_scan_prompts_filter_by_language(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"], include_prompt_docs=False)
    loader.scan()
    assert len(loader.prompts) == 3
    assert all(p["language"] == "zh" for p in loader.prompts.values())


def test_search_by_title(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("代码审查")
    assert len(results) >= 1
    assert any("代码审查" in r["title"] for r in results)


def test_search_by_tag_from_directory(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("编程")
    assert len(results) >= 1


def test_search_returns_fields(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("项目上下文")
    assert len(results) >= 1
    r = results[0]
    for field in ("id", "title", "path", "category", "language", "tags", "summary", "content", "size"):
        assert field in r


def test_search_no_match(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("不存在的关键词xyz")
    assert results == []


def test_search_category_filter(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("文档", category="coding")
    assert all(r["category"] == "coding" for r in results)


def test_search_returns_top10(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("的")
    assert len(results) <= 10
