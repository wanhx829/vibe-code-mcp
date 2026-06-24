import json
import pytest
from tools.generate_doc import handle


@pytest.mark.asyncio
async def test_generate_project_context():
    result = await handle(
        templates_dir="templates",
        doc_type="context",
        project_name="测试项目",
        project_desc="一个测试项目",
        tech_stack="Python+FastAPI",
    )
    data = json.loads(result)
    assert data["doc_type"] == "context"
    assert "测试项目" in data["content"]
    assert "一个测试项目" in data["content"]
    assert "Python+FastAPI" in data["content"]
    assert "项目概要" in data["content"]


@pytest.mark.asyncio
async def test_generate_doc_missing_params():
    result = await handle(
        templates_dir="templates",
        doc_type="context",
        project_name="",
        project_desc="desc",
    )
    assert "错误" in result


@pytest.mark.asyncio
async def test_generate_doc_unsupported_type():
    result = await handle(
        templates_dir="templates",
        doc_type="nonexistent",
        project_name="test",
        project_desc="desc",
    )
    assert "不支持" in result or "错误" in result


@pytest.mark.asyncio
async def test_generate_doc_default_tech_stack():
    result = await handle(
        templates_dir="templates",
        doc_type="context",
        project_name="测试",
        project_desc="描述",
    )
    data = json.loads(result)
    assert "（待填写）" in data["content"]


@pytest.mark.asyncio
async def test_generate_doc_date_substitution():
    result = await handle(
        templates_dir="templates",
        doc_type="context",
        project_name="测试",
        project_desc="描述",
    )
    data = json.loads(result)
    from datetime import date
    assert date.today().isoformat() in data["content"]


@pytest.mark.asyncio
async def test_generate_doc_whitespace_name():
    result = await handle(
        templates_dir="templates",
        doc_type="context",
        project_name="   ",
        project_desc="desc",
    )
    assert "错误" in result
