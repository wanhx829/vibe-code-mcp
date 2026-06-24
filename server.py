import asyncio
import json
import os
import sys

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from resources.config import load_config
from resources.prompt_loader import PromptLoader
from resources.skill_loader import SkillLoader
from resources.doc_loader import DocLoader
from tools import search_prompts, search_skills, search_docs, generate_doc

CONFIG_PATH = os.environ.get("VIBE_CONFIG", os.path.join(os.path.dirname(__file__), "config.yaml"))

try:
    config = load_config(CONFIG_PATH)
except Exception as e:
    print(f"配置加载失败 ({CONFIG_PATH}): {e}", file=sys.stderr)
    sys.exit(1)
RESOURCE_PATH = config["resource_path"]
LANGUAGES = config["scan"]["languages"]
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")

prompt_loader = PromptLoader(RESOURCE_PATH, LANGUAGES, include_prompt_docs=config["scan"]["include_prompt_docs"])
skill_loader = SkillLoader(RESOURCE_PATH, LANGUAGES)
doc_loader = DocLoader(RESOURCE_PATH, LANGUAGES)

server = Server(config["server"]["name"])


@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="search_prompts",
            description="搜索 AI 编程提示词库。当用户需要编程帮助、代码生成、架构设计、调试等场景时调用。",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词或需求描述（中文/英文均可）"},
                    "category": {
                        "type": "string",
                        "description": "提示词分类：coding/system/user/meta/all",
                        "default": "all",
                    },
                    "language": {"type": "string", "description": "语言：zh/en", "default": "zh"},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="search_skills",
            description="查询 AI 技能库。当用户需要特定领域专业知识时调用（数据库、加密货币、Bot 开发、Claude 使用等）。",
            inputSchema={
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "技能关键词（如 postgresql、telegram、ccxt）"},
                    "language": {"type": "string", "description": "语言：zh/en", "default": "zh"},
                },
                "required": ["keyword"],
            },
        ),
        Tool(
            name="search_docs",
            description="检索方法论、经验总结和模板资源。当用户需要编程方法论、项目模板、最佳实践时调用。",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {"type": "string", "description": "搜索主题（如 开发经验、代码组织、项目架构）"},
                    "doc_type": {
                        "type": "string",
                        "description": "文档类型：methodology/template/tutorial/all",
                        "default": "all",
                    },
                    "language": {"type": "string", "description": "语言：zh/en", "default": "zh"},
                },
                "required": ["topic"],
            },
        ),
        Tool(
            name="generate_project_doc",
            description="生成标准化项目文档。当用户启动新项目或需要规范化文档时调用。",
            inputSchema={
                "type": "object",
                "properties": {
                    "doc_type": {
                        "type": "string",
                        "description": "文档类型：context（项目上下文）/ plan（实施计划）/ architecture（架构文档）",
                    },
                    "project_name": {"type": "string", "description": "项目名称"},
                    "project_desc": {"type": "string", "description": "项目简要描述"},
                    "tech_stack": {"type": "string", "description": "技术栈（可选）", "default": ""},
                },
                "required": ["doc_type", "project_name", "project_desc"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "search_prompts":
            result = await search_prompts.handle(
                prompt_loader,
                query=arguments.get("query", ""),
                category=arguments.get("category", "all"),
                language=arguments.get("language", "zh"),
            )
        elif name == "search_skills":
            result = await search_skills.handle(
                skill_loader,
                keyword=arguments.get("keyword", ""),
                language=arguments.get("language", "zh"),
            )
        elif name == "search_docs":
            result = await search_docs.handle(
                doc_loader,
                topic=arguments.get("topic", ""),
                doc_type=arguments.get("doc_type", "all"),
                language=arguments.get("language", "zh"),
            )
        elif name == "generate_project_doc":
            result = await generate_doc.handle(
                templates_dir=TEMPLATES_DIR,
                doc_type=arguments.get("doc_type", ""),
                project_name=arguments.get("project_name", ""),
                project_desc=arguments.get("project_desc", ""),
                tech_stack=arguments.get("tech_stack", ""),
            )
        else:
            result = json.dumps({"错误": f"未知工具: {name}"}, ensure_ascii=False)
    except Exception as e:
        result = json.dumps({"错误": f"工具执行失败: {e}"}, ensure_ascii=False)

    return [TextContent(type="text", text=result)]


async def main():
    prompt_loader.scan()
    skill_loader.scan()
    doc_loader.scan()
    print(
        f"Vibe Coding MCP Server 启动完成: "
        f"{len(prompt_loader.prompts)} 提示词, "
        f"{len(skill_loader.skills)} 技能, "
        f"{len(doc_loader.docs)} 文档",
        file=sys.stderr,
    )
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
