# Vibe Code MCP Server 生成指南

> 本文档是一份完整的 AI 可执行指南。当您拥有一个 vibecodingcn 源码项目时，AI 可以按照本文档的步骤，从零生成完整的 MCP Server 项目。

---

## 目录

1. [项目概述](#1-项目概述)
2. [前置条件](#2-前置条件)
3. [设计阶段提示词](#3-设计阶段提示词)
4. [实施计划](#4-实施计划)
5. [完整源码](#5-完整源码)
6. [测试套件](#6-测试套件)
7. [配置与部署文件](#7-配置与部署文件)
8. [验证与测试](#8-验证与测试)
9. [Claude CLI 集成](#9-claude-cli-集成)
10. [GitHub 发布](#10-github-发布)
11. [实施过程中的修复记录](#11-实施过程中的修复记录)

---

## 1. 项目概述

### 1.1 目标

构建一个 Python MCP Server（`vibe-code-mcp`），将 vibecodingcn 的提示词库、Skills 技能库、方法论文档和模板资源暴露为 MCP 工具，供 Claude CLI 调用。

### 1.2 核心设计决策

| 决策项 | 选择 | 理由 |
|--------|------|------|
| 工具形态 | Python MCP Server | Claude CLI 原生支持，跨平台，无需额外运行时 |
| 工具组织 | 4 个独立工具 | 每个工具职责单一，Claude 更容易精准选择 |
| 匹配机制 | Claude 自主决策 | Claude 本身就是最好的意图理解器，无需额外 embedding 模型 |
| 资源定位 | 配置文件指定路径 | 可移植到任何机器，修改 config.yaml 即可 |
| 默认语言 | 中文 | 用户主力语言为中文 |

### 1.3 技术栈

- Python 3.10+
- `mcp` SDK >= 1.0.0
- `pyyaml` >= 6.0
- `pytest` + `pytest-asyncio`（开发依赖）

### 1.4 功能特性

- **4 个 MCP 工具**：提示词搜索、技能查询、文档检索、项目文档生成
- **多语言支持**：中文/英文资源自动索引
- **智能搜索**：基于标题、标签、摘要、内容的加权匹配
- **零外部依赖**：仅需 `mcp` + `pyyaml`，无需数据库
- **跨平台**：Windows / macOS / Linux 均可运行

---

## 2. 前置条件

### 2.1 vibecodingcn 资源目录结构

MCP Server 需要访问 vibecodingcn 的资源目录，其结构如下：

```
vibecodingcn/
├── i18n/
│   ├── zh/
│   │   ├── prompts/                  # 中文提示词
│   │   │   ├── coding_prompts/       # 编程类提示词
│   │   │   ├── system_prompts/       # 系统类提示词
│   │   │   ├── user_prompts/         # 用户类提示词
│   │   │   └── meta_prompts/         # 元提示词
│   │   ├── skills/                   # 中文技能
│   │   │   └── <skill_name>/
│   │   │       ├── SKILL.md          # 技能定义（含 YAML frontmatter）
│   │   │       └── references/       # 参考文档
│   │   └── documents/                # 中文文档
│   │       ├── Methodology and Principles/   # 方法论
│   │       ├── Templates and Resources/      # 模板
│   │       └── Tutorials and Guides/         # 教程
│   └── en/
│       ├── prompts/                  # 英文提示词
│       ├── skills/                   # 英文技能
│       └── documents/                # 英文文档
└── libs/
    └── external/
        └── prompts-library/
            └── prompt_docs/          # 大型提示词库（可选）
```

### 2.2 资源文件格式说明

**提示词文件**（`.md`）：
- 第一行以 `# ` 开头的是标题
- 文件名格式：`(序号,序号)_标题.md`
- 内容为 Markdown 格式

**技能文件**（`SKILL.md`）：
- 包含 YAML frontmatter：`name` 和 `description` 字段
- 目录下可有 `references/` 子目录存放参考文档

**文档文件**（`.md`）：
- 第一行以 `# ` 开头的是标题
- 按目录名分类：`Methodology and Principles`、`Templates and Resources`、`Tutorials and Guides`

---

## 3. 设计阶段提示词

### 3.1 初始需求提示词

```
构建一个 Python MCP Server，将 vibecodingcn 的提示词库、Skills 技能库、方法论文档和模板资源暴露为结构化工具，供 Claude CLI 通过 MCP 协议调用。

核心目标：
- 在任意目录启动 Claude CLI 时，可调用 vibecodingcn 的全部资源
- Claude 根据用户输入自主选择工具和查询关键词，MCP Server 只负责检索和返回
- 通过配置文件指定资源路径，可在任意环境中部署使用

需要 4 个工具：
1. search_prompts - 搜索提示词库
2. search_skills - 查询技能库
3. search_docs - 检索方法论和模板
4. generate_project_doc - 生成标准化项目文档
```

### 3.2 设计审查提示词

```
审查这个 MCP Server 设计：
- 架构是否合理？
- 工具定义是否清晰？
- 资源索引机制是否高效？
- 搜索算法是否足够？
- 错误处理是否完善？
- 是否有遗漏的场景？
```

### 3.3 实施计划生成提示词

```
将设计文档转化为详细的实施计划：
- 每个任务要小到可以在 2-5 分钟内完成
- 使用 TDD 方式：先写测试，再写实现
- 每个任务完成后提交一次 commit
- 包含完整的代码块，不要有占位符
```

---

## 4. 实施计划

### 4.1 文件结构

```
mcp-server/
├── server.py                 # MCP Server 入口
├── config.yaml               # 配置文件
├── requirements.txt          # 生产依赖
├── requirements-dev.txt      # 开发依赖
├── pytest.ini                # 测试配置
├── README.md                 # 使用说明
├── LICENSE                   # MIT 许可证
├── .gitignore                # Git 忽略规则
├── MCP-GENERATION-GUIDE.md   # 本文件
├── resources/
│   ├── __init__.py           # 空文件
│   ├── config.py             # 配置加载器
│   ├── prompt_loader.py      # 提示词索引与搜索
│   ├── skill_loader.py       # 技能索引与搜索
│   └── doc_loader.py         # 文档索引与搜索
├── tools/
│   ├── __init__.py           # 空文件
│   ├── search_prompts.py     # 提示词搜索工具
│   ├── search_skills.py      # 技能搜索工具
│   ├── search_docs.py        # 文档搜索工具
│   └── generate_doc.py       # 文档生成工具
├── templates/
│   └── project_context.md    # 项目上下文模板
└── tests/
    ├── __init__.py           # 空文件
    ├── conftest.py           # 共享测试夹具
    ├── test_config.py
    ├── test_prompt_loader.py
    ├── test_skill_loader.py
    ├── test_doc_loader.py
    ├── test_search_prompts.py
    ├── test_search_skills.py
    ├── test_search_docs.py
    └── test_generate_doc.py
```

### 4.2 实施任务清单

| 任务 | 内容 | 文件数 | 测试数 |
|------|------|--------|--------|
| Task 1 | 项目脚手架 & 配置加载器 | 8 | 4 |
| Task 2 | 提示词加载器 | 3 | 10 |
| Task 3 | 技能加载器 | 3 | 6 |
| Task 4 | 文档加载器 | 3 | 8 |
| Task 5 | search_prompts & search_skills 工具 | 4 | 6 |
| Task 6 | search_docs & generate_project_doc 工具 | 5 | 6 |
| Task 7 | MCP Server 入口 | 1 | 0 |
| Task 8 | README & 最终验证 | 1 | 0 |
| **合计** | | **28** | **43** |

---

## 5. 完整源码

### 5.1 `resources/config.py` — 配置加载器

```python
import os
import yaml


DEFAULTS = {
    "default_language": "zh",
    "server": {"name": "vibe-coding", "version": "1.0.0"},
    "scan": {
        "include_prompt_docs": True,
        "max_summary_length": 500,
        "languages": ["zh", "en"],
    },
}


def load_config(config_path: str) -> dict:
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    if not config or "resource_path" not in config:
        raise ValueError("config.yaml must contain 'resource_path'")

    resource_path = config["resource_path"]
    if not os.path.isdir(resource_path):
        raise FileNotFoundError(f"resource_path does not exist: {resource_path}")

    for key, value in DEFAULTS.items():
        if key not in config:
            config[key] = value
        elif isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if sub_key not in config[key]:
                    config[key][sub_key] = sub_value

    return config
```

### 5.2 `resources/prompt_loader.py` — 提示词索引与搜索

```python
import os
import re


CATEGORY_MAP = {
    "coding_prompts": "coding",
    "system_prompts": "system",
    "user_prompts": "user",
    "meta_prompts": "meta",
}


class PromptLoader:
    def __init__(self, resource_path: str, languages: list[str] | None = None, include_prompt_docs: bool = True):
        self.resource_path = resource_path
        self.languages = languages or ["zh", "en"]
        self.include_prompt_docs = include_prompt_docs
        self.prompts: dict[str, dict] = {}

    def scan(self):
        self.prompts.clear()
        for lang in self.languages:
            prompts_dir = os.path.join(self.resource_path, "i18n", lang, "prompts")
            if not os.path.isdir(prompts_dir):
                continue
            for category_dir in os.listdir(prompts_dir):
                category_path = os.path.join(prompts_dir, category_dir)
                if not os.path.isdir(category_path):
                    continue
                category = CATEGORY_MAP.get(category_dir, category_dir)
                for fname in os.listdir(category_path):
                    if not fname.endswith(".md"):
                        continue
                    fpath = os.path.join(category_path, fname)
                    self._index_file(fpath, category, lang)

        if self.include_prompt_docs:
            self._scan_prompt_docs()

    def _scan_prompt_docs(self):
        prompt_docs_dir = os.path.join(
            self.resource_path, "libs", "external", "prompts-library", "prompt_docs"
        )
        if not os.path.isdir(prompt_docs_dir):
            return
        for root, _dirs, files in os.walk(prompt_docs_dir):
            for fname in files:
                if not fname.endswith(".md"):
                    continue
                fpath = os.path.join(root, fname)
                self._index_file(fpath, "prompt_docs", "mixed")

    def _index_file(self, fpath: str, category: str, language: str):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError):
            return

        title = self._extract_title(content, fpath)
        summary = self._extract_summary(content, max_length=500)
        tags = self._extract_tags(fpath, category)

        file_id = f"{category}_{language}_{os.path.basename(fpath)}"
        self.prompts[file_id] = {
            "id": file_id,
            "title": title,
            "path": fpath,
            "category": category,
            "language": language,
            "tags": tags,
            "summary": summary,
            "content": content,
            "size": len(content.encode("utf-8")),
        }

    def search(self, query: str, category: str = "all", limit: int = 10) -> list[dict]:
        query_lower = query.lower()
        results = []
        for entry in self.prompts.values():
            if category != "all" and entry["category"] != category:
                continue
            score = 0
            if query_lower in entry["title"].lower():
                score += 3
            if any(query_lower in tag.lower() for tag in entry["tags"]):
                score += 2
            if query_lower in entry["summary"].lower():
                score += 1
            if score > 0:
                results.append((score, entry))
        results.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in results[:limit]]

    @staticmethod
    def _extract_title(content: str, fpath: str) -> str:
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
        basename = os.path.basename(fpath)
        return re.sub(r"^\(\d+,\d+\)_", "", basename).replace(".md", "").replace("_", " ").strip()

    @staticmethod
    def _extract_summary(content: str, max_length: int = 500) -> str:
        text = content.lstrip()
        if text.startswith("---"):
            parts = text.split("---", 2)
            text = parts[2].lstrip() if len(parts) >= 3 else text
        text = text[:max_length]
        last_period = max(text.rfind("。"), text.rfind(". "), text.rfind("\n"))
        if last_period > 50:
            text = text[:last_period + 1]
        return text.strip()

    @staticmethod
    def _extract_tags(fpath: str, category: str) -> list[str]:
        tags = []
        category_labels = {
            "coding": "编程",
            "system": "系统",
            "user": "用户",
            "meta": "元提示词",
        }
        if category in category_labels:
            tags.append(category_labels[category])
        basename = os.path.basename(fpath)
        name = re.sub(r"^\(\d+,\d+\)_", "", basename).replace(".md", "")
        parts = re.split(r"[_\s]+", name)
        tags.extend(p for p in parts if len(p) > 1)
        return tags
```

### 5.3 `resources/skill_loader.py` — 技能索引与搜索

```python
import os
import re


class SkillLoader:
    def __init__(self, resource_path: str, languages: list[str] | None = None):
        self.resource_path = resource_path
        self.languages = languages or ["zh", "en"]
        self.skills: dict[str, dict] = {}

    def scan(self):
        self.skills.clear()
        for lang in self.languages:
            skills_dir = os.path.join(self.resource_path, "i18n", lang, "skills")
            if not os.path.isdir(skills_dir):
                continue
            for entry in os.listdir(skills_dir):
                skill_path = os.path.join(skills_dir, entry)
                if not os.path.isdir(skill_path):
                    continue
                skill_md = os.path.join(skill_path, "SKILL.md")
                if not os.path.isfile(skill_md):
                    continue
                self._index_skill(skill_md, entry, lang)

    def _index_skill(self, skill_md: str, skill_name: str, language: str):
        try:
            with open(skill_md, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError):
            return

        title, description = self._parse_frontmatter(content, skill_name)
        references = self._scan_references(os.path.dirname(skill_md))

        self.skills[skill_name] = {
            "id": skill_name,
            "title": title,
            "path": skill_md,
            "domain": description,
            "language": language,
            "size": len(content.encode("utf-8")),
            "content": content,
            "references": references,
        }

    def search(self, keyword: str, limit: int = 10) -> list[dict]:
        keyword_lower = keyword.lower()
        results = []
        for entry in self.skills.values():
            score = 0
            if keyword_lower in entry["id"].lower():
                score += 3
            if keyword_lower in entry["title"].lower():
                score += 3
            if keyword_lower in entry["domain"].lower():
                score += 2
            if keyword_lower in entry["content"].lower():
                score += 1
            if score > 0:
                results.append((score, entry))
        results.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in results[:limit]]

    @staticmethod
    def _parse_frontmatter(content: str, fallback_name: str) -> tuple[str, str]:
        title = fallback_name
        description = ""
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                fm = parts[1]
                for line in fm.strip().split("\n"):
                    if line.startswith("name:"):
                        title = line.split(":", 1)[1].strip().strip('"')
                    elif line.startswith("description:"):
                        description = line.split(":", 1)[1].strip().strip('"')
        if not title:
            title = fallback_name
        return title, description

    @staticmethod
    def _scan_references(skill_dir: str) -> list[dict]:
        refs = []
        ref_dir = os.path.join(skill_dir, "references")
        if not os.path.isdir(ref_dir):
            return refs
        for fname in os.listdir(ref_dir):
            if fname.endswith(".md"):
                refs.append({
                    "title": fname.replace(".md", ""),
                    "path": os.path.join(ref_dir, fname),
                })
        return refs
```

### 5.4 `resources/doc_loader.py` — 文档索引与搜索

```python
import os
import re


TYPE_MAP = {
    "Methodology and Principles": "methodology",
    "Templates and Resources": "template",
    "Tutorials and Guides": "tutorial",
}


class DocLoader:
    def __init__(self, resource_path: str, languages: list[str] | None = None):
        self.resource_path = resource_path
        self.languages = languages or ["zh", "en"]
        self.docs: dict[str, dict] = {}

    def scan(self):
        self.docs.clear()
        for lang in self.languages:
            docs_dir = os.path.join(self.resource_path, "i18n", lang, "documents")
            if not os.path.isdir(docs_dir):
                continue
            for type_dir in os.listdir(docs_dir):
                type_path = os.path.join(docs_dir, type_dir)
                if not os.path.isdir(type_path):
                    continue
                doc_type = TYPE_MAP.get(type_dir, "other")
                for fname in os.listdir(type_path):
                    if not fname.endswith(".md"):
                        continue
                    fpath = os.path.join(type_path, fname)
                    self._index_file(fpath, doc_type, lang)

    def _index_file(self, fpath: str, doc_type: str, language: str):
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
        except (OSError, UnicodeDecodeError):
            return

        title = self._extract_title(content, fpath)
        summary = self._extract_summary(content, max_length=500)
        tags = self._extract_tags(fpath, doc_type)

        file_id = f"{doc_type}_{language}_{os.path.basename(fpath)}"
        self.docs[file_id] = {
            "id": file_id,
            "title": title,
            "path": fpath,
            "type": doc_type,
            "language": language,
            "tags": tags,
            "summary": summary,
            "content": content,
            "size": len(content.encode("utf-8")),
        }

    def search(self, topic: str, doc_type: str = "all", limit: int = 10) -> list[dict]:
        topic_lower = topic.lower()
        results = []
        for entry in self.docs.values():
            if doc_type != "all" and entry["type"] != doc_type:
                continue
            score = 0
            if topic_lower in entry["title"].lower():
                score += 3
            if any(topic_lower in tag.lower() for tag in entry["tags"]):
                score += 2
            if topic_lower in entry["summary"].lower():
                score += 1
            if topic_lower in entry["content"].lower():
                score += 1
            if score > 0:
                results.append((score, entry))
        results.sort(key=lambda x: x[0], reverse=True)
        return [entry for _, entry in results[:limit]]

    @staticmethod
    def _extract_title(content: str, fpath: str) -> str:
        for line in content.split("\n"):
            line = line.strip()
            if line.startswith("# "):
                return line[2:].strip()
        basename = os.path.basename(fpath)
        return re.sub(r"^\(\d+,\d+\)_", "", basename).replace(".md", "").replace("_", " ").strip()

    @staticmethod
    def _extract_summary(content: str, max_length: int = 500) -> str:
        text = content.lstrip()
        if text.startswith("---"):
            parts = text.split("---", 2)
            text = parts[2].lstrip() if len(parts) >= 3 else text
        text = text[:max_length]
        last_period = max(text.rfind("。"), text.rfind(". "), text.rfind("\n"))
        if last_period > 50:
            text = text[:last_period + 1]
        return text.strip()

    @staticmethod
    def _extract_tags(fpath: str, doc_type: str) -> list[str]:
        tags = []
        type_labels = {
            "methodology": "方法论",
            "template": "模板",
            "tutorial": "教程",
        }
        if doc_type in type_labels:
            tags.append(type_labels[doc_type])
        basename = os.path.basename(fpath).replace(".md", "")
        parts = basename.replace("_", " ").split()
        tags.extend(p for p in parts if len(p) > 1)
        return tags
```

### 5.5 `tools/search_prompts.py` — 提示词搜索工具

```python
import json


async def handle(prompt_loader, query: str, category: str = "all", language: str = "zh") -> str:
    if not query or not query.strip():
        return json.dumps({"错误": "query 参数不能为空"}, ensure_ascii=False)

    results = prompt_loader.search(query.strip(), category=category)
    if not results:
        return json.dumps({"结果": [], "提示": "未找到匹配的提示词，建议换关键词试试"}, ensure_ascii=False)

    return json.dumps(results, ensure_ascii=False)
```

### 5.6 `tools/search_skills.py` — 技能搜索工具

```python
import json


async def handle(skill_loader, keyword: str, language: str = "zh") -> str:
    if not keyword or not keyword.strip():
        return json.dumps({"错误": "keyword 参数不能为空"}, ensure_ascii=False)

    results = skill_loader.search(keyword.strip())
    return json.dumps(results, ensure_ascii=False)
```

### 5.7 `tools/search_docs.py` — 文档搜索工具

```python
import json


async def handle(doc_loader, topic: str, doc_type: str = "all", language: str = "zh") -> str:
    if not topic or not topic.strip():
        return json.dumps({"错误": "topic 参数不能为空"}, ensure_ascii=False)

    results = doc_loader.search(topic.strip(), doc_type=doc_type)
    return json.dumps(results, ensure_ascii=False)
```

### 5.8 `tools/generate_doc.py` — 文档生成工具

```python
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
```

### 5.9 `server.py` — MCP Server 入口

```python
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
```

### 5.10 `templates/project_context.md` — 项目上下文模板

```markdown
# {{project_name}} 项目上下文文档

## 项目概要

- **项目名称**：{{project_name}}
- **项目描述**：{{project_desc}}
- **技术栈**：{{tech_stack}}
- **创建时间**：{{date}}

## 项目背景

（待填写：要解决的问题、现有方案的不足、项目的独特价值）

## 技术栈

| 层级 | 选型 | 说明 |
|------|------|------|
| 前端 | （待填写） | - |
| 后端 | （待填写） | - |
| 数据库 | （待填写） | - |
| 基础设施 | （待填写） | - |

## 架构设计

（待填写：模块划分、核心交互流程、数据流向）

## 功能需求

### 核心功能（P0）

1. （待填写）

### 增强功能（P1）

1. （待填写）

## 非功能需求

- **性能**：（待填写）
- **安全**：（待填写）
- **可用性**：（待填写）

## 开发规范

- **代码风格**：遵循项目既有规范
- **Git 工作流**：功能分支 → Code Review → 合并主分支
- **测试要求**：核心功能必须有测试覆盖

## 里程碑

| 阶段 | 内容 | 预计时间 |
|------|------|----------|
| M1 | 核心功能开发 | - |
| M2 | 测试与优化 | - |
| M3 | 上线部署 | - |
```

---

## 6. 测试套件

### 6.1 `tests/conftest.py` — 共享测试夹具

```python
import os
import pytest


@pytest.fixture
def resource_dir(tmp_path):
    """Create a minimal vibecodingcn resource structure for testing."""
    zh_prompts = tmp_path / "i18n" / "zh" / "prompts" / "coding_prompts"
    zh_prompts.mkdir(parents=True)

    (zh_prompts / "(1,1)_项目上下文与代码审查.md").write_text(
        "# 项目上下文与代码审查\n\n将自然语言需求转换为结构化项目上下文文档。帮助进行代码审查，发现潜在问题。",
        encoding="utf-8",
    )

    en_prompts = tmp_path / "i18n" / "en" / "prompts" / "coding_prompts"
    en_prompts.mkdir(parents=True)
    (en_prompts / "(1,1)_project_context.md").write_text(
        "# Project Context Generator\n\nGenerate structured project context documents.",
        encoding="utf-8",
    )

    zh_system = tmp_path / "i18n" / "zh" / "prompts" / "system_prompts"
    zh_system.mkdir(parents=True)
    (zh_system / "(1,1)_系统架构分析.md").write_text(
        "# 系统架构分析\n\n分析系统架构，提供优化建议。",
        encoding="utf-8",
    )

    zh_meta = tmp_path / "i18n" / "zh" / "prompts" / "meta_prompts"
    zh_meta.mkdir(parents=True)
    (zh_meta / "(1,1)_提示词优化.md").write_text(
        "# 提示词优化\n\n优化现有提示词，提升效果。",
        encoding="utf-8",
    )

    # External prompt_docs library
    prompt_docs = tmp_path / "libs" / "external" / "prompts-library" / "prompt_docs" / "subdir"
    prompt_docs.mkdir(parents=True)
    (prompt_docs / "架构设计提示词.md").write_text(
        "# 架构设计提示词\n\n帮助进行系统架构设计。",
        encoding="utf-8",
    )

    # Skills
    zh_skills = tmp_path / "i18n" / "zh" / "skills"
    zh_skills.mkdir(parents=True)
    pg_skill = zh_skills / "postgresql"
    pg_skill.mkdir()
    (pg_skill / "SKILL.md").write_text(
        "---\nname: postgresql\ndescription: \"PostgreSQL 专家技能\"\n---\n\n# PostgreSQL 专家\n\nPostgreSQL 数据库最佳实践。",
        encoding="utf-8",
    )
    refs = pg_skill / "references"
    refs.mkdir()
    (refs / "cli.md").write_text("# CLI Reference\n\npsql commands.", encoding="utf-8")

    en_skills = tmp_path / "i18n" / "en" / "skills"
    en_skills.mkdir(parents=True)
    ccxt_skill = en_skills / "ccxt"
    ccxt_skill.mkdir()
    (ccxt_skill / "SKILL.md").write_text(
        "---\nname: ccxt\ndescription: \"Crypto exchange API\"\n---\n\n# CCXT\n\nUnified crypto exchange API.",
        encoding="utf-8",
    )

    # Documents
    zh_docs = tmp_path / "i18n" / "zh" / "documents"
    methodology = zh_docs / "Methodology and Principles"
    methodology.mkdir(parents=True)
    (methodology / "开发经验.md").write_text(
        "# 开发经验\n\n变量命名、文件结构、编码规范、架构原则等实践经验。",
        encoding="utf-8",
    )
    (methodology / "编程之道.md").write_text(
        "# 编程之道\n\n编程哲学与思维方式。",
        encoding="utf-8",
    )

    templates = zh_docs / "Templates and Resources"
    templates.mkdir(parents=True)
    (templates / "通用项目架构模板.md").write_text(
        "# 通用项目架构模板\n\n适用于各类项目的架构设计模板。",
        encoding="utf-8",
    )

    tutorials = zh_docs / "Tutorials and Guides"
    tutorials.mkdir(parents=True)
    (tutorials / "快速入门.md").write_text(
        "# 快速入门\n\n新手入门教程。",
        encoding="utf-8",
    )

    return tmp_path
```

### 6.2 `tests/test_config.py`

```python
import os
import pytest
import yaml
from resources.config import load_config


def test_load_config_reads_yaml(tmp_path):
    config_data = {
        "resource_path": str(tmp_path),
        "default_language": "zh",
        "server": {"name": "test", "version": "0.1.0"},
        "scan": {
            "include_prompt_docs": False,
            "max_summary_length": 300,
            "languages": ["zh"],
        },
    }
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.dump(config_data, allow_unicode=True), encoding="utf-8")

    config = load_config(str(config_file))
    assert config["resource_path"] == str(tmp_path)
    assert config["default_language"] == "zh"
    assert config["server"]["name"] == "test"
    assert config["scan"]["languages"] == ["zh"]


def test_load_config_validates_resource_path(tmp_path):
    config_data = {"resource_path": "/nonexistent/path/that/does/not/exist"}
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.dump(config_data), encoding="utf-8")

    with pytest.raises(FileNotFoundError):
        load_config(str(config_file))


def test_load_config_missing_file():
    with pytest.raises(FileNotFoundError):
        load_config("/nonexistent/config.yaml")


def test_load_config_default_values(tmp_path):
    config_data = {"resource_path": str(tmp_path)}
    config_file = tmp_path / "config.yaml"
    config_file.write_text(yaml.dump(config_data), encoding="utf-8")

    config = load_config(str(config_file))
    assert config["default_language"] == "zh"
    assert config["server"]["name"] == "vibe-coding"
    assert config["server"]["version"] == "1.0.0"
    assert config["scan"]["include_prompt_docs"] is True
    assert config["scan"]["max_summary_length"] == 500
    assert config["scan"]["languages"] == ["zh", "en"]
```

### 6.3 `tests/test_prompt_loader.py`

```python
from resources.prompt_loader import PromptLoader


def test_scan_prompts(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh", "en"])
    loader.scan()
    assert len(loader.prompts) == 5  # 4 i18n + 1 prompt_docs


def test_scan_prompts_includes_prompt_docs(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"], include_prompt_docs=True)
    loader.scan()
    prompt_docs = [p for p in loader.prompts.values() if p["category"] == "prompt_docs"]
    assert len(prompt_docs) == 1
    assert "架构设计" in prompt_docs[0]["title"]


def test_scan_prompts_excludes_prompt_docs(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"], include_prompt_docs=False)
    loader.scan()
    prompt_docs = [p for p in loader.prompts.values() if p["category"] == "prompt_docs"]
    assert len(prompt_docs) == 0


def test_scan_prompts_filter_by_language(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"], include_prompt_docs=False)
    loader.scan()
    assert len(loader.prompts) == 3
    assert all(p["language"] == "zh" for p in loader.prompts.values())


def test_search_by_title(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("代码审查")
    assert len(results) >= 1
    assert any("代码审查" in r["title"] for r in results)


def test_search_by_tag_from_directory(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("编程")
    assert len(results) >= 1


def test_search_returns_fields(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("项目上下文")
    assert len(results) >= 1
    r = results[0]
    for field in ("id", "title", "path", "category", "language", "tags", "summary", "content", "size"):
        assert field in r


def test_search_no_match(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("不存在的关键词xyz")
    assert results == []


def test_search_category_filter(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("文档", category="coding")
    assert all(r["category"] == "coding" for r in results)


def test_search_returns_top10(resource_dir):
    loader = PromptLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("的")
    assert len(results) <= 10
```

### 6.4 `tests/test_skill_loader.py`

```python
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
```

### 6.5 `tests/test_doc_loader.py`

```python
from resources.doc_loader import DocLoader


def test_scan_docs(resource_dir):
    loader = DocLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    assert len(loader.docs) == 4


def test_search_by_topic(resource_dir):
    loader = DocLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("开发经验")
    assert len(results) >= 1
    assert any("开发经验" in r["title"] for r in results)


def test_search_filter_by_type(resource_dir):
    loader = DocLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("模板", doc_type="template")
    assert all(r["type"] == "template" for r in results)


def test_search_returns_fields(resource_dir):
    loader = DocLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("开发经验")
    assert len(results) >= 1
    r = results[0]
    for field in ("id", "title", "path", "type", "language", "tags", "summary", "content", "size"):
        assert field in r


def test_search_no_match(resource_dir):
    loader = DocLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("不存在的主题xyz")
    assert results == []


def test_search_respects_limit(resource_dir):
    loader = DocLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("的", limit=1)
    assert len(results) == 1


def test_search_content_match(resource_dir):
    loader = DocLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("编码规范")
    assert len(results) >= 1
    assert any("编码规范" in r["content"] for r in results)


def test_search_ordering_by_relevance(resource_dir):
    """Verify that a title match (score 3) ranks higher than a summary/content-only match (score 1+1)."""
    docs_dir = resource_dir / "i18n" / "zh" / "documents" / "Methodology and Principles"
    (docs_dir / "编码规范指南.md").write_text(
        "# 编码规范指南\n\n详细的编码规范说明。",
        encoding="utf-8",
    )
    loader = DocLoader(str(resource_dir), languages=["zh"])
    loader.scan()
    results = loader.search("编码规范")
    assert len(results) >= 2
    assert "编码规范指南" in results[0]["title"]
```

### 6.6 `tests/test_search_prompts.py`

```python
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
    assert data == []
```

### 6.7 `tests/test_search_skills.py`

```python
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
```

### 6.8 `tests/test_search_docs.py`

```python
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
```

### 6.9 `tests/test_generate_doc.py`

```python
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
```

---

## 7. 配置与部署文件

### 7.1 `config.yaml`

```yaml
resource_path: "D:/wsl/workspace/vibecodingcn"
default_language: "zh"

server:
  name: "vibe-code-mcp"
  version: "1.0.0"

scan:
  include_prompt_docs: true
  max_summary_length: 500
  languages: ["zh", "en"]
```

### 7.2 `requirements.txt`

```
mcp>=1.0.0
pyyaml>=6.0
```

### 7.3 `requirements-dev.txt`

```
-r requirements.txt
pytest>=7.0
pytest-asyncio>=0.21
```

### 7.4 `pytest.ini`

```ini
[pytest]
asyncio_mode = auto
```

### 7.5 `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Testing
.pytest_cache/
.coverage
*.cover
*.py,cover
.hypothesis/

# Logs
*.log
*.log.[0-9]*
*.out

# Environment
.env
.env.local
.env.*.local

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# OS
.DS_Store
Thumbs.db
```

### 7.6 `LICENSE`

```
MIT License

Copyright (c) 2026 Vibe Coding

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 7.7 空 `__init__.py` 文件

以下三个文件需要创建为空文件（0 字节）：

- `resources/__init__.py`
- `tools/__init__.py`
- `tests/__init__.py`

---

## 8. 验证与测试

### 8.1 安装依赖

```bash
cd mcp-server
pip install -r requirements-dev.txt
```

### 8.2 运行测试

```bash
cd mcp-server
python -m pytest tests/ -v
```

预期输出：43 个测试全部通过。

### 8.3 测试启动

```bash
cd mcp-server
python server.py
```

预期输出（stderr）：
```
Vibe Coding MCP Server 启动完成: N 提示词, M 技能, K 文档
```

按 Ctrl+C 退出。

---

## 9. Claude CLI 集成

### 9.1 用户级配置

编辑 `~/.claude/settings.json`：

```json
{
  "mcpServers": {
    "vibe-code-mcp": {
      "command": "python",
      "args": ["D:/wsl/workspace/vibecodingcn/mcp-server/server.py"],
      "env": {
        "VIBE_CONFIG": "D:/wsl/workspace/vibecodingcn/mcp-server/config.yaml"
      }
    }
  }
}
```

### 9.2 项目级配置

在项目根目录创建 `.claude/settings.json`，内容同上。

### 9.3 验证 MCP Server

在 Claude CLI 中输入：

```
帮我搜索架构设计相关的提示词
```

Claude 应自动调用 `search_prompts` 工具并返回结果。

---

## 10. GitHub 发布

### 10.1 创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名：`vibe-code-mcp`
3. 描述：`MCP Server for vibecodingcn - AI 编程提示词与技能库`
4. 选择 Public 或 Private
5. 不要初始化 README/LICENSE/.gitignore（本地已有）

### 10.2 上传代码

```bash
cd D:/wsl/workspace/vibecodingcn

# 初始化 Git（如果还没有）
git init

# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/vibe-code-mcp.git

# 添加 MCP Server 目录
git add mcp-server/

# 提交
git commit -m "feat: vibe-code-mcp - MCP Server for vibecodingcn"

# 推送
git push -u origin main
```

### 10.3 README.md

项目 README 已包含在 `mcp-server/README.md` 中，包含：
- 功能特性
- 快速开始指南
- 可用工具说明
- 项目结构
- 开发指南
- 移植说明

---

## 11. 实施过程中的修复记录

在开发过程中发现并修复了以下问题，AI 在重新生成时应直接使用修复后的代码：

### 11.1 `generate_doc.py` 返回类型不一致

**问题**：成功时返回原始 Markdown 字符串，错误时返回 JSON 字符串，类型不一致。

**修复**：成功时也返回 JSON 格式：
```python
return json.dumps({"content": template, "doc_type": doc_type}, ensure_ascii=False)
```

**影响**：测试也需要更新，先 `json.loads(result)` 再断言 `data["content"]`。

### 11.2 `server.py` 缺少错误处理

**问题**：`call_tool` 没有 try/except，模块级 `load_config` 也没有错误处理。

**修复**：
- `call_tool` 外层包裹 `try/except Exception`，返回 JSON 错误信息
- `load_config` 包裹 `try/except`，失败时打印 stderr 并 `sys.exit(1)`

### 11.3 `file_id` 格式防碰撞

**问题**：`file_id` 使用 `{category}_{basename}` 格式，中英文同名文件会冲突。

**修复**：改为 `{category}_{language}_{basename}` 格式：
```python
file_id = f"{category}_{language}_{os.path.basename(fpath)}"
```

### 11.4 异常类型精确化

**问题**：loader 中使用裸 `except Exception` 会捕获不该捕获的异常。

**修复**：改为 `except (OSError, UnicodeDecodeError)`。

### 11.5 `search_skills` 和 `search_docs` 工具缺少空结果提示

**问题**：`search_prompts` 有空结果友好提示，但 `search_skills` 和 `search_docs` 没有。

**修复**：在 `search_prompts.py` 中保留友好提示，`search_skills.py` 和 `search_docs.py` 直接返回空列表（由 Claude 自行解释）。

---

## 附录：搜索权重说明

### 提示词搜索权重

| 匹配位置 | 权重 |
|----------|------|
| 标题 | +3 |
| 标签 | +2 |
| 摘要 | +1 |

### 技能搜索权重

| 匹配位置 | 权重 |
|----------|------|
| ID（目录名） | +3 |
| 标题 | +3 |
| 领域描述 | +2 |
| 内容 | +1 |

### 文档搜索权重

| 匹配位置 | 权重 |
|----------|------|
| 标题 | +3 |
| 标签 | +2 |
| 摘要 | +1 |
| 内容 | +1 |

---

## 附录：MCP 工具参数速查

### search_prompts

```json
{
  "query": "架构设计",           // 必填
  "category": "all",            // 可选：coding/system/user/meta/all
  "language": "zh"              // 可选：zh/en
}
```

### search_skills

```json
{
  "keyword": "postgresql",      // 必填
  "language": "zh"              // 可选：zh/en
}
```

### search_docs

```json
{
  "topic": "开发经验",           // 必填
  "doc_type": "all",            // 可选：methodology/template/tutorial/all
  "language": "zh"              // 可选：zh/en
}
```

### generate_project_doc

```json
{
  "doc_type": "context",        // 必填：context
  "project_name": "我的项目",    // 必填
  "project_desc": "项目描述",    // 必填
  "tech_stack": "React+Node"    // 可选
}
```
