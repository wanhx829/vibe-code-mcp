import json
import pytest
from unittest.mock import MagicMock
from tools.search_skills import handle


@pytest.mark.asyncio
async def test_search_skills_success():
    mock_loader = MagicMock()
    mock_loader.search.return_value = [
        {"id": "postgresql", "title": "PostgreSQL", "path": "/pg/SKILL.md",
         "domain": "数据库", "language": "zh", "size": 76000, "content": "...", "references": []}
    ]
    result = await handle(mock_loader, keyword="postgresql", language="zh")
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["id"] == "postgresql"


@pytest.mark.asyncio
async def test_search_skills_missing_keyword():
    mock_loader = MagicMock()
    result = await handle(mock_loader, keyword="", language="zh")
    assert "错误" in result


@pytest.mark.asyncio
async def test_search_skills_no_match():
    mock_loader = MagicMock()
    mock_loader.search.return_value = []
    result = await handle(mock_loader, keyword="nonexistent", language="zh")
    data = json.loads(result)
    assert data == []
