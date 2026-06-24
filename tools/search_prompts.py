import json


async def handle(prompt_loader, query: str, category: str = "all", language: str = "zh") -> str:
    if not query or not query.strip():
        return json.dumps({"错误": "query 参数不能为空"}, ensure_ascii=False)

    results = prompt_loader.search(query.strip(), category=category)
    if not results:
        return json.dumps({"结果": [], "提示": "未找到匹配的提示词，建议换关键词试试"}, ensure_ascii=False)

    return json.dumps(results, ensure_ascii=False)
