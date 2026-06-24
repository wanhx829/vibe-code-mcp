import json


async def handle(doc_loader, topic: str, doc_type: str = "all", language: str = "zh") -> str:
    if not topic or not topic.strip():
        return json.dumps({"错误": "topic 参数不能为空"}, ensure_ascii=False)

    results = doc_loader.search(topic.strip(), doc_type=doc_type)
    return json.dumps(results, ensure_ascii=False)
