import json
import pytest
from unittest.mock import MagicMock
from tools.search_docs import handle


@pytest.mark.asyncio
async def test_search_docs_success():
    mock_loader = MagicMock()
    mock_loader.search.return_value = [
        {"id": "m1", "title": "开发经验", "path": "/d.md", "type": "methodology",
         "language": "zh", "tags": ["方法论"], "summary": "编码规范", "content": "...", "size": 100}
    ]
    result = await handle(mock_loader, topic="开发经验", doc_type="all", language="zh")
    data = json.loads(result)
    assert len(data) == 1
    assert data[0]["title"] == "开发经验"


@pytest.mark.asyncio
async def test_search_docs_missing_topic():
    mock_loader = MagicMock()
    result = await handle(mock_loader, topic="", doc_type="all", language="zh")
    assert "错误" in result


@pytest.mark.asyncio
async def test_search_docs_no_match():
    mock_loader = MagicMock()
    mock_loader.search.return_value = []
    result = await handle(mock_loader, topic="不存在", doc_type="all", language="zh")
    data = json.loads(result)
    assert data == []
