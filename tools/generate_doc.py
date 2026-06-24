import json
import os
from datetime import date


async def handle(
    templates_dir: str,
    doc_type: str,
    project_name: str,
    project_desc: str,
    tech_stack: str = "",
) -> str:
    if not project_name or not project_name.strip():
        return json.dumps({"错误": "project_name 不能为空"}, ensure_ascii=False)
    if not project_desc or not project_desc.strip():
        return json.dumps({"错误": "project_desc 不能为空"}, ensure_ascii=False)

    template_file = os.path.join(templates_dir, f"project_{doc_type}.md")
    if not os.path.exists(template_file):
        return json.dumps({"错误": f"不支持的文档类型: {doc_type}，目前支持: context"}, ensure_ascii=False)

    with open(template_file, "r", encoding="utf-8") as f:
        template = f.read()

    template = template.replace("{{project_name}}", project_name.strip())
    template = template.replace("{{project_desc}}", project_desc.strip())
    template = template.replace("{{tech_stack}}", tech_stack or "（待填写）")
    template = template.replace("{{date}}", date.today().isoformat())

    return json.dumps({"content": template, "doc_type": doc_type}, ensure_ascii=False)
