# Vibe Code MCP Server

将 AI 编程提示词库、技能库、方法论文档和模板资源暴露为 MCP 工具，供 Claude CLI 调用。

## 功能特性

- **4 个 MCP 工具**：提示词搜索、技能查询、文档检索、项目文档生成
- **中文资源**：内置中文提示词、技能和文档资源
- **智能搜索**：基于标题、标签、摘要、内容的加权匹配
- **零外部依赖**：仅需 `mcp` + `pyyaml`，无需数据库
- **跨平台**：Windows / macOS / Linux 均可运行

## 快速开始

### 1. 安装依赖

```bash
cd vibe-code-mcp
pip install -r requirements.txt
```

### 2. 测试启动

```bash
python server.py
```

预期输出（stderr）：
```
Vibe Coding MCP Server 启动完成: 47 提示词, 14 技能, 17 文档
```

按 Ctrl+C 退出。

## 可用工具

### search_prompts

搜索 AI 编程提示词库。

**参数**：
- `query` (必填)：搜索关键词或需求描述
- `category` (可选)：提示词分类 - coding/system/user/meta/all
- `language` (可选)：语言 - zh

**示例**：
```json
{
  "query": "架构设计",
  "category": "all",
  "language": "zh"
}
```

### search_skills

查询 AI 技能库。

**参数**：
- `keyword` (必填)：技能关键词
- `language` (可选)：语言 - zh

**示例**：
```json
{
  "keyword": "postgresql",
  "language": "zh"
}
```

### search_docs

检索方法论、经验总结和模板资源。

**参数**：
- `topic` (必填)：搜索主题
- `doc_type` (可选)：文档类型 - methodology/template/tutorial/all
- `language` (可选)：语言 - zh

**示例**：
```json
{
  "topic": "开发经验",
  "doc_type": "all",
  "language": "zh"
}
```

### generate_project_doc

生成标准化项目文档。

**参数**：
- `doc_type` (必填)：文档类型 - context
- `project_name` (必填)：项目名称
- `project_desc` (必填)：项目简要描述
- `tech_stack` (可选)：技术栈

**示例**：
```json
{
  "doc_type": "context",
  "project_name": "我的项目",
  "project_desc": "一个示例项目",
  "tech_stack": "React+Node"
}
```

## Claude CLI 集成

### 用户级配置

编辑 `~/.claude/settings.json`：

```json
{
  "mcpServers": {
    "vibe-code-mcp": {
      "command": "python",
      "args": ["D:/path/to/vibe-code-mcp/server.py"],
      "env": {
        "VIBE_CONFIG": "D:/path/to/vibe-code-mcp/config.yaml"
      }
    }
  }
}
```

### 项目级配置

在项目根目录创建 `.claude/settings.json`，内容同上。

### 验证

在 Claude CLI 中输入：

```
帮我搜索架构设计相关的提示词
```

Claude 应自动调用 `search_prompts` 工具并返回结果。

## 项目结构

```
vibe-code-mcp/
├── server.py                 # MCP Server 入口
├── config.yaml               # 配置文件
├── requirements.txt          # 生产依赖
├── requirements-dev.txt      # 开发依赖
├── pytest.ini                # 测试配置
├── README.md                 # 本文件
├── USAGE.md                  # 详细使用手册
├── LICENSE                   # MIT 许可证
├── .gitignore                # Git 忽略规则
├── MCP-GENERATION-GUIDE.md   # 生成指南
├── data/                     # 内置资源
│   └── i18n/
│       └── zh/               # 中文资源
│           ├── prompts/      # 提示词库
│           ├── skills/       # 技能库
│           └── documents/    # 文档库
├── resources/
│   ├── __init__.py
│   ├── config.py             # 配置加载器
│   ├── prompt_loader.py      # 提示词索引与搜索
│   ├── skill_loader.py       # 技能索引与搜索
│   └── doc_loader.py         # 文档索引与搜索
├── tools/
│   ├── __init__.py
│   ├── search_prompts.py     # 提示词搜索工具
│   ├── search_skills.py      # 技能搜索工具
│   ├── search_docs.py        # 文档搜索工具
│   └── generate_doc.py       # 文档生成工具
├── templates/
│   └── project_context.md    # 项目上下文模板
└── tests/
    ├── __init__.py
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

## 开发指南

### 运行测试

```bash
cd vibe-code-mcp
pip install -r requirements-dev.txt
python -m pytest tests/ -v
```

预期输出：43 个测试全部通过。

### 添加新工具

1. 在 `tools/` 目录创建新文件
2. 实现 `handle` 异步函数
3. 在 `server.py` 的 `list_tools` 和 `call_tool` 中注册
4. 添加对应测试

### 添加新资源

1. 在 `data/i18n/zh/` 目录下添加对应的 `.md` 文件
2. 重启 MCP Server 自动索引

## 搜索权重说明

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

## 许可证

MIT License
