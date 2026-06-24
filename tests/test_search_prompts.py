import json
import pytest
from unittest.mock import MagicMock
from tools.search_prompts import handle


@pytest.mark.asyncio
async def test_search_prompts_success():
    mock_loader = MagicMock()
    mock_loader.search.return_value = [
        {"id": "c1", "title": "项目上下文", "path": "/a.md", "category": "coding",
         "language": "zh", "tags": ["编程"], "summary": "生成项目文档", "content": "...", "size": 100}
    ]
    result = await handle(mock_loader, query="项目上下文", category="all", language="zh")
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["title"] == "项目上下文"


@pytest.mark.asyncio
async def test_search_prompts_missing_query():
    mock_loader = MagicMock()
    result = await handle(mock_loader, query="", category="all", language="zh")
    assert "错误" in result


@pytest.mark.asyncio
async def test_search_prompts_no_match():
    mock_loader = MagicMock()
    mock_loader.search.return_value = []
    result = await handle(mock_loader, query="不存在", category="all", language="zh")
    data = json.loads(result)
    assert data["结果"] == []
    assert "提示" in data
