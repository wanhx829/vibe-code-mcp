import json


async def handle(skill_loader, keyword: str, language: str = "zh") -> str:
    if not keyword or not keyword.strip():
        return json.dumps({"错误": "keyword 参数不能为空"}, ensure_ascii=False)

    results = skill_loader.search(keyword.strip())
    return json.dumps(results, ensure_ascii=False)
