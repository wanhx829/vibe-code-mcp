# 中文 AI 资源发现清单

发现日期：2026-06-24

## 筛选目标

本轮只做资源发现，不直接导入 `vibe-code-mcp`。筛选依据如下：

- GitHub star 数较高，或在 AI 编程/MCP/Agent 细分领域高相关。
- 中文可读，适合中国开发者直接使用。
- 能转化为 MCP 中的 `skills`、`prompts`、`documents` 或模板。
- 优先选择有结构、有目录、有许可证或明确说明的项目。
- 排除明显不适合作为默认资源的项目，例如盗版书库、政治内容、
  纯娱乐 prompt、低质量搬运、无结构长列表。

## 第一批优先候选

### 1. datawhalechina/hello-agents

- 地址：[datawhalechina/hello-agents](https://github.com/datawhalechina/hello-agents)
- 当前星标：约 61.3k
- 类型：Agent 原理与实践教程
- 适合导入：`skills/agent-engineering`、`documents/agent-guide`
- 价值判断：高

建议提取内容：

- Agent 基础概念。
- Agent 架构与经典范式。
- 多智能体应用构建流程。
- Agent 任务拆解、工具调用、记忆与协作机制。

导入方式：

- 不复制全文。
- 先做一个 `agent-engineering` skill 入口。
- 将关键章节整理为 references。
- 在 MCP 中只返回摘要和引用入口。

### 2. datawhalechina/happy-llm

- 地址：[datawhalechina/happy-llm](https://github.com/datawhalechina/happy-llm)
- 当前星标：约 31.5k
- 类型：从零开始构建大模型教程
- 适合导入：`documents/llm-fundamentals`
- 价值判断：中高

建议提取内容：

- LLM 基础术语。
- Transformer 与训练基础。
- 模型构建流程。
- 与 AI 编程相关的上下文、推理、生成机制解释。

导入方式：

- 只提炼成 MCP 可检索文档，不建议作为 coding skill。
- 面向“解释模型能力边界”“理解 token/context”的场景。

### 3. datawhalechina/self-llm

- 地址：[datawhalechina/self-llm](https://github.com/datawhalechina/self-llm)
- 当前星标：约 31k
- 类型：开源大模型部署、微调、应用教程
- 适合导入：`skills/local-llm`、`documents/local-llm-guide`
- 价值判断：中高

建议提取内容：

- 本地 LLM 环境配置。
- 开源模型部署。
- LoRA / 全量微调基础。
- LangChain 等应用接入流程。

导入方式：

- 新建 `local-llm` skill。
- references 按部署、微调、调用、常见问题拆分。
- 默认不返回超长命令清单，避免污染上下文。

### 4. datawhalechina/llm-cookbook

- 地址：[datawhalechina/llm-cookbook](https://github.com/datawhalechina/llm-cookbook)
- 当前星标：约 24.3k
- 类型：面向开发者的 LLM 入门手册
- 适合导入：`skills/llm-app-development`、`prompts/llm-app`
- 价值判断：高

建议提取内容：

- Prompt Engineering。
- RAG 开发。
- LLM 应用开发。
- 微调基础。
- 国内开发者适配经验。

导入方式：

- 优先抽取 Prompt、RAG、应用开发三部分。
- 形成三个轻量 skill：
  - `prompt-engineering`
  - `rag-development`
  - `llm-app-development`

### 5. jnMetaCode/agency-agents-zh

- 地址：[jnMetaCode/agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh)
- 当前星标：约 15.5k
- 类型：AI 专家角色库
- 适合导入：`prompts/roles`、`skills/multi-agent-workflow`
- 价值判断：高，但需要治理

建议提取内容：

- 工程、产品、设计、安全等专家角色。
- 每个角色的专业流程和交付物定义。
- 多角色协作方式。

风险：

- 角色数量很大，不能全文导入默认索引。
- 需要筛选与软件工程直接相关的角色。

导入方式：

- 先挑 10 到 20 个工程相关角色。
- 转成结构化 role prompt。
- 加 `use_when`、`avoid_when`、`token_cost`。

### 6. WangRongsheng/awesome-LLM-resources

- 地址：[WangRongsheng/awesome-LLM-resources](https://github.com/WangRongsheng/awesome-LLM-resources)
- 当前星标：约 8.6k
- 类型：LLM 资源总表
- 适合导入：`documents/llm-resource-index`
- 价值判断：中

建议提取内容：

- 多模态、Agent、辅助编程、AI 审稿、数据处理、模型训练、
  模型推理、MCP 等资源索引。

导入方式：

- 不直接导入全文。
- 作为“外部资源索引”保留链接。
- MCP 搜索时可作为推荐来源，而不是主上下文。

### 7. adongwanai/AgentGuide

- 地址：[adongwanai/AgentGuide](https://github.com/adongwanai/AgentGuide)
- 当前星标：约 6.2k
- 类型：AI Agent 开发与面试指南
- 适合导入：`skills/context-engineering`、`skills/agent-eval`
- 价值判断：高

建议提取内容：

- Agent Loop。
- LangGraph / OpenAI Agents SDK。
- MCP / Skills / 权限与状态管理。
- Context Engineering。
- RAG / Multimodal RAG。
- Eval / Observability / Safety。

导入方式：

- 优先抽取 context engineering、tool loadout、成本控制、
  eval 和安全边界。
- 与当前 MCP “省 token、工作更完整”的目标强相关。

### 8. jnMetaCode/superpowers-zh

- 地址：[jnMetaCode/superpowers-zh](https://github.com/jnMetaCode/superpowers-zh)
- 当前星标：约 5.8k
- 类型：AI 编程 skills 方法论中文增强版
- 适合导入：`skills/code-review`、`skills/debugging`、
  `skills/tdd`、`skills/mcp-builder`
- 价值判断：高，但需注意同质化

建议提取内容：

- 头脑风暴。
- TDD。
- 调试。
- 代码审查。
- MCP 服务器构建。
- 工作流执行器。

风险：

- 与本仓现有 AI 编程方法论有部分重叠。
- 需要融合，不应简单复制。

导入方式：

- 对照现有 `i18n/zh/skills/claude-skills` 和 coding prompts。
- 提炼缺口，形成短入口 skill。
- references 中标注来源和许可证。

### 9. KimYx0207/AI-Coding-Guide-Zh

- 地址：[KimYx0207/AI-Coding-Guide-Zh](https://github.com/KimYx0207/AI-Coding-Guide-Zh)
- 当前星标：约 4.9k
- 类型：Claude Code + OpenClaw + Codex 中文教程
- 适合导入：`documents/ai-coding-workflow`
- 价值判断：高

建议提取内容：

- Claude Code 编程线。
- OpenClaw 助手线。
- Codex Agent 线。
- 团队规范和安全边界。
- 工具选择与权限边界。

导入方式：

- 优先整理“按身份选择路线”和团队落地部分。
- 适合作为 MCP 的 workflow 推荐依据。

### 10. datawhalechina/Agent-Learning-Hub

- 地址：[datawhalechina/Agent-Learning-Hub](https://github.com/datawhalechina/Agent-Learning-Hub)
- 当前星标：约 4.1k
- 类型：AI Agent 学习路线与资料库
- 适合导入：`documents/agent-resource-index`
- 价值判断：中高

建议提取内容：

- Claude Code、learn-claude-code、OpenClaw、Hermes Agent 等
  agent harness 学习入口。
- Agent 学习路线。
- 工具生态索引。

导入方式：

- 只作为索引型文档。
- 不进入默认 prompt/skill。

### 11. liaokongVFX/MCP-Chinese-Getting-Started-Guide

- 地址：[liaokongVFX/MCP-Chinese-Getting-Started-Guide](https://github.com/liaokongVFX/MCP-Chinese-Getting-Started-Guide)
- 当前星标：约 3.5k
- 类型：MCP 中文极速入门
- 适合导入：`skills/mcp-development`
- 价值判断：高

建议提取内容：

- MCP 核心概念。
- Resources / Prompts / Tools / Sampling / Roots / Transports。
- stdio 与 SSE。
- MCP Server 工具设计。

导入方式：

- 新建 `mcp-development` skill。
- 先提炼工具设计、schema、stdio 调试。
- 与官方 MCP 文档形成双来源。

### 12. cfrs2005/claude-init

- 地址：[cfrs2005/claude-init](https://github.com/cfrs2005/claude-init)
- 当前星标：约 1.4k
- 类型：Claude Code 中文开发套件
- 适合导入：`documents/claude-code-setup`
- 价值判断：中

建议提取内容：

- 中文初始化模板。
- MCP 服务器集成。
- 智能上下文管理。
- 安全扫描。

风险：

- 项目 README 显示“归档说明：仅供学习参考”。
- 不建议作为长期依赖，只能参考设计。

### 13. stormzhang/ai-coding-guide

- 地址：[stormzhang/ai-coding-guide](https://github.com/stormzhang/ai-coding-guide)
- 当前星标：约 1.2k
- 类型：AI 编程 CLI 中文教程
- 适合导入：`documents/ai-coding-cli-guide`
- 价值判断：中高

建议提取内容：

- Claude Code + Codex 的入门路线。
- CLI 使用方式。
- 面向小白的解释和实践路径。

导入方式：

- 作为教程型文档索引。
- 不建议复制大量正文。

### 14. IsHexx/system-prompts-and-models-of-ai-tools-chinese

- 地址：[IsHexx/system-prompts-and-models-of-ai-tools-chinese](https://github.com/IsHexx/system-prompts-and-models-of-ai-tools-chinese)
- 当前星标：约 1.1k
- 类型：AI 编程工具系统提示词中文合集
- 适合导入：`documents/ai-tool-system-prompts`
- 价值判断：中，但必须谨慎

建议提取内容：

- Cursor、Devin、VSCode Agent、Replit、Windsurf 等工具提示词。
- AI 编程工具内部工作机制参考。

风险：

- 项目包含系统提示词和模型文档，可能存在来源、版权、合规问题。
- 不建议直接导入 prompt 内容。

导入方式：

- 只做“研究参考索引”。
- 不进入默认搜索结果。
- 若提取，只提炼设计模式，不复制原始提示词。

## 官方与英文高质量补充源

这些不是中文资源，但应作为质量校准来源：

### modelcontextprotocol/servers

- 地址：[modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
- 当前星标：约 87.6k
- 类型：MCP reference servers
- 用途：校准 MCP Server 设计、工具 schema、参考实现。
- 导入方式：只作为 `mcp-development` skill 的官方引用。

### modelcontextprotocol/python-sdk

- 地址：[modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk)
- 当前星标：约 23.4k
- 类型：MCP Python SDK
- 用途：校准当前 Python MCP 实现。
- 导入方式：只作为 `mcp-development` skill 的官方引用。

### dair-ai/Prompt-Engineering-Guide

- 地址：[dair-ai/Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide)
- 当前星标：约 75.9k
- 类型：Prompt Engineering / RAG / Agent 资源
- 用途：校准 prompt engineering skill。
- 导入方式：只作为参考，不全文导入。

## 推荐导入顺序

### 第一批：直接补 MCP 缺口

1. `mcp-development`
   - 来源：MCP 中文极速入门、官方 MCP servers、Python SDK。
   - 目标：补齐当前 MCP 自身建设能力。

2. `context-engineering`
   - 来源：AgentGuide、AI-Coding-Guide-Zh。
   - 目标：解决 token 节省、上下文选择、长任务压缩。

3. `agent-engineering`
   - 来源：hello-agents、Agent-Learning-Hub、AgentGuide。
   - 目标：补齐 Agent 工作流、工具调用、记忆与协作。

4. `code-review`
   - 来源：superpowers-zh、AI-Coding-Guide-Zh、当前仓库经验文档。
   - 目标：让 AI 不只写代码，也能稳定审查。

5. `debugging`
   - 来源：superpowers-zh、当前仓库开发经验。
   - 目标：建立可复现、可验证的调试流程。

### 第二批：应用开发能力

1. `prompt-engineering`
2. `rag-development`
3. `llm-app-development`
4. `local-llm`
5. `multi-agent-workflow`

### 第三批：索引型资源

1. `llm-resource-index`
2. `agent-resource-index`
3. `ai-coding-cli-guide`
4. `ai-tool-system-prompts`

## 不建议直接导入的内容

- 原始泄露类 system prompts。
- 未明确授权或许可证混乱的提示词全文。
- 超长 awesome list 全文。
- 只按 star 高但与 MCP 目标无关的 NLP 数据集。
- 过于偏模型训练而非 AI 编程工作流的材料。

## 下一步动作

建议下一步先做 `mcp-development` 和 `context-engineering` 两个 skill：

1. 每个 skill 只写 80 到 150 行入口 `SKILL.md`。
2. 每个 skill 配 3 到 5 个 references。
3. references 只放提炼后的要点，不搬运全文。
4. 给每个资源记录来源 URL、许可证、适用场景和风险等级。
5. 在 MCP 搜索中默认返回摘要，不返回全文。

这样能先解决当前 MCP 自身最大问题：资源越多，越容易浪费 token。
