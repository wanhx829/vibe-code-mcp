from resources.skill_loader import SkillLoader


def test_scan_skills(resource_dir):
    loader = SkillLoader(str(resource_dir), languages=["zh", "en"])
    loader.scan()
    assert len(loader.skills) == 2


def test_scan_skills_filter_by_language(resource_dir):
    loader = SkillLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    assert len(loader.skills) == 1


def test_search_by_name(resource_dir):
    loader = SkillLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("postgresql")
    assert len(results) == 1
    assert results[0]["id"] == "postgresql"


def test_search_by_content(resource_dir):
    loader = SkillLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("数据库")
    assert len(results) >= 1


def test_search_returns_fields(resource_dir):
    loader = SkillLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("postgresql")
    assert len(results) == 1
    r = results[0]
    for field in ("id", "title", "path", "domain", "language", "size", "content", "references"):
        assert field in r


def test_search_no_match(resource_dir):
    loader = SkillLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("nonexistent_skill_xyz")
    assert results == []
