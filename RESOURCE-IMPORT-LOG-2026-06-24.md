# 中文 AI 资源导入记录

导入日期：2026-06-24

## 导入范围

本次将第一批高相关中文 AI 资源转入 `vibe-code-mcp` 的内置
skills 体系。导入目标是先补齐 MCP 的功能覆盖：Agent、上下文工程、
MCP 开发、Prompt、RAG、LLM 应用、代码审查和调试。

本次不复制外部仓库全文，而是提炼为可被 MCP 检索的 `SKILL.md`
和 `references/`。这样既能让功能先完整，又保留后续继续扩展的空间。

## 外部来源

- datawhalechina/hello-agents
- datawhalechina/llm-cookbook
- adongwanai/AgentGuide
- jnMetaCode/superpowers-zh
- liaokongVFX/MCP-Chinese-Getting-Started-Guide

## 新增 Skills

- `agent-engineering`：
  来源 hello-agents、AgentGuide。用于 Agent 架构、工具、记忆、评估。
- `context-engineering`：
  来源 AgentGuide、hello-agents。用于上下文选择、压缩、长任务维护。
- `mcp-development`：
  来源 MCP 中文入门、superpowers-zh。用于 MCP Server 设计、schema、调试。
- `prompt-engineering`：
  来源 llm-cookbook、当前提示词库。用于 Prompt 结构、优化、评估。
- `rag-development`：
  来源 llm-cookbook、AgentGuide。用于 RAG pipeline、分块、引用、评估。
- `llm-app-development`：
  来源 llm-cookbook、hello-agents。用于 LLM 应用架构、工具调用、运维。
- `code-review`：
  来源 superpowers-zh、当前项目规范。用于代码审查、风险分级、中文表达。
- `debugging`：
  来源 superpowers-zh。用于根因定位、复现、验证和回归。

## 新增文件数量

- 新增 skill：8 个。
- 新增 skill 文件总数：32 个。
- 每个 skill 包含 1 个 `SKILL.md` 和 3 个 `references/` 文件。

## 许可证处理

- `hello-agents`：发现 `LICENSE.txt`，许可证为 CC BY-NC-SA 4.0。
- `superpowers-zh`：发现 `LICENSE`，许可证为 MIT。
- `AgentGuide`：根目录未发现 LICENSE。
- `llm-cookbook`：根目录未发现 LICENSE。
- `MCP-Chinese-Getting-Started-Guide`：根目录未发现 LICENSE。

处理策略：

- 对未发现 LICENSE 的来源，只做摘要、索引和工程化重组。
- 不搬运外部仓库全文。
- 每个新增 skill 的 `references/source-map.md` 记录了来源和许可证状态。

## 验证结果

已执行：

```bash
python - <<'PY'
from resources.skill_loader import SkillLoader
loader = SkillLoader('./data', ['zh'])
loader.scan()
print(len(loader.skills))
PY
```

结果：`22`，技能数从 14 增加到 22。

已执行新增文件 lint：

```bash
find data/i18n/zh/skills \
  -path '*/agent-engineering/*' -o \
  -path '*/context-engineering/*' -o \
  -path '*/mcp-development/*' -o \
  -path '*/prompt-engineering/*' -o \
  -path '*/rag-development/*' -o \
  -path '*/llm-app-development/*' -o \
  -path '*/code-review/*' -o \
  -path '*/debugging/*' \
  | sort | xargs npx markdownlint
```

结果：通过。

关键词召回已验证：

- `agent` 命中 `agent-engineering`。
- `上下文` 命中 `context-engineering`。
- `mcp` 命中 `mcp-development`。
- `prompt` 命中 `prompt-engineering`。
- `rag` 命中 `rag-development`。
- `llm` 命中 `llm-app-development`。
- `代码审查` 命中 `code-review`。
- `调试` 命中 `debugging`。

## 后续建议

下一步可以开始改 MCP 工具层：

1. `search_skills` 增加 `limit` 和 `language` 过滤。
2. 增加 `get_skill_reference`，让新增 references 能按需读取。
3. 增加 `search_context`，统一召回 skills、prompts、documents。
4. 再考虑 token 优化，把搜索默认返回从全文改为 metadata。
