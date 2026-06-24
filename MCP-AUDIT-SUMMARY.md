# Vibe Code MCP 审查总结

审查日期：2026-06-24

## 结论

当前 `vibe-code-mcp` 已经具备最小可用 MCP 形态：能启动一个
Python stdio MCP Server，并暴露提示词搜索、技能查询、文档检索、
项目上下文文档生成 4 个工具。内置中文资源与主仓 `i18n/zh`
当前数量基本同步：47 个提示词、14 个技能、17 篇文档，技能引用
资料和脚本也已随资源一起复制。

但它还没有达到“完整、好用、节省 token、让 AI 工作更完整”的
目标。主要问题不是资源数量，而是工具粒度、检索质量、返回内容
控制、资源治理和工作流闭环不足。当前工具会把完整 `content`
直接返回，单个结果可能达到几十 KB，例如 `postgresql` 技能约
75 KB、系统架构 Mermaid 提示词约 34 KB。这会显著浪费上下文，
并让模型更难稳定选择关键片段。

建议定位为：先把它从“资源全文搜索器”升级为“分层检索与工作流导航器”，再继续补充 prompts 和 skills。

## 已完成情况

### 资源覆盖

- 中文提示词：47 个，覆盖架构、计划、任务描述、前端设计、代码规范、文档生成等方向。
- 中文技能：14 个，包括 PostgreSQL、TimescaleDB、Telegram、CCXT、
  Polymarket、Hummingbot、Claude 使用、Claude Skills 等。
- 中文文档：17 篇，覆盖方法论、模板、教程和工具配置。
- 技能附属资料：`references/` 数量与主仓一致，当前共 92 个 Markdown 引用文件。
- 技能脚本：数量与主仓一致，当前共 4 个脚本文件。

### 工具能力

- `search_prompts`：按标题、标签、摘要做简单加权匹配。
- `search_skills`：按 skill id、标题、description、全文做简单匹配。
- `search_docs`：按标题、标签、摘要、全文做简单匹配。
- `generate_project_doc`：支持生成项目上下文文档。

### 测试与文档

- 仓库包含 pytest 测试，README 声称共有 43 个测试。
- README、USAGE、MCP-GENERATION-GUIDE 已覆盖 Claude CLI 和 Codex CLI 集成说明。

## 关键问题

### P0：返回全文导致 token 浪费

当前搜索工具返回结果对象时包含完整 `content`。这会造成两个直接问题：

- 搜索阶段就消耗大量 token，而搜索阶段通常只需要标题、摘要、路径、标签、评分和资源 id。
- 多个大资源命中时，模型容易被低相关长文本稀释注意力。

建议改为两阶段读取：

- 默认搜索只返回 metadata：`id`、`title`、`summary`、
  `category/type/domain`、`tags`、`size`、`score`、`path`。
- 新增 `get_prompt`、`get_skill`、`get_doc`、`get_reference`，按 id 精确读取内容。
- 精确读取也要支持 `max_chars`、`section`、`include_references`、`summary_only`。

### P0：检索质量偏弱

当前检索基本是 `query in title/tag/summary/content` 的子串匹配。抽查结果：

- `架构设计` 只命中少量提示词，不能稳定召回“系统架构”“通用项目架构模板”等相关资源。
- `代码组织` 在 prompts 中无结果，但 documents 中有结果。
- `前端` 在 skills 中无结果，即使前端是高频开发场景。
- `PostgreSQL` 在 prompts 中无结果，只能依赖 skill。

建议增强：

- 增加关键词切分、同义词表和中英文别名，例如 `架构=architecture=系统设计`、`计划=plan=实施计划`、`前端=frontend=UI`。
- 搜索结果返回 `score` 和 `matched_fields`，让调用方知道为什么命中。
- 支持 `limit`、`offset`、`min_score`，避免固定返回 10 条。
- 对标题、文件名、frontmatter tags、摘要、正文分段分别建索引。

### P0：缺少工作流级工具

当前工具只解决“找资料”，没有解决“AI 应该如何使用资料”。要让 MCP 真正提升 AI 编程效果，需要加入工作流型工具：

- `create_project_brief`：把用户一句话需求扩展为项目上下文草案。
- `create_implementation_plan`：生成分阶段实施计划和验收标准。
- `review_project_structure`：根据项目目录给出结构审查与补齐建议。
- `select_relevant_context`：根据任务自动推荐 prompts、skills、docs 的组合。
- `generate_agent_instructions`：生成或更新 `AGENTS.md` / `CLAUDE.md` / `GEMINI.md`。
- `compress_context`：把长文档压缩为适合当前任务的短上下文。

### P1：文档声明与实际能力不一致

- `server.py` 的 `generate_project_doc` schema 描述了
  `context / plan / architecture`，但实际只有 `project_context.md`
  模板，传入 `plan` 或 `architecture` 会报不支持。
- README/USAGE 多处强调 `zh/en` 或多语言，但当前 `config.yaml` 只扫描 `zh`，内置数据也只有 `zh`。
- README 启动依赖于 `pyyaml` 和 `mcp`，当前环境未安装依赖时
  无法直接运行；审查时 `python -m pytest` 也因缺少 `pytest`
  无法执行。

建议修正文档或补齐能力，二者至少要一致。

### P1：资源治理不足

- 默认内置了一个明显不适合作为通用 system prompt 的高风险文件。
  文件位于 `data/i18n/zh/prompts/system_prompts/`，文件名包含私密、
  攻击性和实验性叙事元素。建议移出默认索引，或标记为
  `unsafe/private/experimental`。
- 存在目录名 `system_prompts/CLAUDE.md/`，它不是 Markdown 文件，
  当前 loader 会忽略它。需要明确这是预期资源还是历史残留。
- 缺少资源 manifest，无法表达资源用途、质量等级、风险等级、适用场景、是否默认启用。

建议新增 `resources.yaml` 或每个资源的 frontmatter，字段包括：

- `title`
- `description`
- `tags`
- `use_when`
- `avoid_when`
- `risk_level`
- `token_cost`
- `source`
- `version`
- `default_enabled`

### P1：引用资料不可按需读取

`SkillLoader` 会列出 `references` 的路径，但没有工具读取某个引用
文件。对大型 skill 来说，最佳使用方式应该是先读 `SKILL.md` 的
入口说明，再按任务读取引用资料。当前只能通过全文返回或路径提示
间接处理，MCP 用户体验不完整。

建议新增：

- `list_skill_references(skill_id)`
- `get_skill_reference(skill_id, reference_id, max_chars=...)`
- `search_skill_references(skill_id, query)`

### P1：缺少同步与更新机制

`vibe-code-mcp/data` 是主仓资源的拷贝，但没有看到自动同步脚本或校验命令。后续主仓 `i18n/zh` 更新后，MCP 很容易变成旧快照。

建议新增：

- `scripts/sync_resources.py`：从主仓复制或筛选资源。
- `scripts/audit_resources.py`：检查数量差异、非法文件名、超大文件、敏感词、缺少 frontmatter。
- `make sync-resources`
- `make audit-resources`
- CI 或本地测试中加入资源一致性检查。

## 建议新增的 MCP 工具

### 第一优先级

1. `list_resources`
   - 返回 prompts、skills、docs、templates 的数量、语言、分类和版本。
   - 用于让模型先了解可用资源，而不是盲搜。

2. `search_context`
   - 统一搜索 prompts、skills、docs，并按任务类型聚合结果。
   - 返回推荐组合，而不是让模型分别调用三个搜索工具。

3. `get_resource`
   - 按 `resource_type + id` 精确读取。
   - 支持 `max_chars`、`summary_only`、`sections`。

4. `get_skill_reference`
   - 读取 skill 的某个引用资料。
   - 支持按引用标题或 id 读取。

5. `recommend_workflow`
   - 输入用户任务，输出推荐流程：先用哪个 prompt、是否需要哪个 skill、需要哪些文档、下一步产物是什么。

### 第二优先级

1. `generate_plan_doc`
   - 补齐 `generate_project_doc` 已声明但未实现的 `plan`。

2. `generate_architecture_doc`
   - 补齐 `architecture`。

3. `generate_agent_rules`
   - 根据项目类型生成 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md` 指令草案。

4. `review_context_pack`
   - 对一个项目的上下文包进行完整性审查。

5. `summarize_resource`
   - 将长 prompt / skill / doc 压缩为当前任务可用摘要。

## 建议新增或重构的 Skills

当前 skills 偏向数据库、量化交易、Telegram、Claude 生态。作为通用 vibe coding MCP，建议补齐软件工程高频场景：

1. `project-planning`
   - 需求澄清、范围切分、里程碑、验收标准、风险登记。

2. `context-engineering`
   - 如何构建项目上下文、如何压缩上下文、如何选择相关文件、如何避免上下文污染。

3. `code-review`
   - 代码审查清单、风险分级、测试缺口、回归风险。

4. `debugging`
   - 复现、假设、最小化、日志定位、二分、修复验证。

5. `testing`
   - 单元测试、集成测试、端到端测试、测试数据、覆盖率策略。

6. `frontend-production`
   - React/Vue/Tailwind/shadcn、响应式布局、可访问性、视觉质量、前端验收。

7. `backend-api`
   - REST/GraphQL、鉴权、错误模型、幂等、分页、限流、OpenAPI。

8. `python-engineering`
   - 包结构、pytest、typing、ruff、uv、日志、配置、CLI。

9. `node-typescript`
   - TS 项目结构、pnpm、eslint、vitest、构建与发布。

10. `security-baseline`
    - secrets、依赖安全、输入校验、权限边界、安全审查。

11. `mcp-development`
    - MCP Server 设计、工具 schema、资源读取、stdio 调试、客户端集成。

12. `documentation`
    - README、API 文档、变更日志、架构决策记录、用户手册。

13. `git-workflow`
    - commit 规范、PR 描述、分支策略、变更拆分。

14. `deployment-ops`
    - Docker、环境变量、日志、健康检查、备份、回滚。

这些 skills 不需要一开始写成长文档。更适合每个 skill 采用轻量入口 + references 的结构，并通过 MCP 按需读取，避免默认加载全文。

## 建议新增或整理的 Prompts

### 应新增的 prompt 类型

1. 项目启动上下文收集 prompt
2. 需求澄清与缺口发现 prompt
3. 实施计划生成 prompt
4. 架构设计审查 prompt
5. 文件级代码审查 prompt
6. PR 审查 prompt
7. Bug 复现与定位 prompt
8. 测试用例生成 prompt
9. 重构计划 prompt
10. 文档生成 prompt
11. 上下文压缩 prompt
12. token 预算控制 prompt
13. MCP 工具设计 prompt
14. AGENTS.md 生成 prompt
15. 多 Agent 分工 prompt

### 应整理的现有 prompt

- 把超长 prompt 拆成入口 prompt、规则模块、输出模板、示例四类。
- 给每个 prompt 增加 tags 和 `use_when`。
- 移除或默认禁用明显私有、玩笑、攻击性、实验性 system prompt。
- 为高频任务建立短 prompt 版本，优先供 MCP 默认返回。
- 对重复的架构、计划、任务描述 prompt 做合并，保留 1 个主版本和若干变体。

## 推荐路线图

### 第 1 阶段：先省 token

- 搜索工具默认不返回 `content`。
- 增加 `get_resource` 精确读取工具。
- 搜索结果增加 `score`、`matched_fields`、`size`、`token_cost_estimate`。
- 所有工具支持 `limit` 和 `max_chars`。

验收标准：

- 搜索一次只返回短 metadata。
- 读取全文必须显式调用精确读取工具。
- `postgresql` 这类大 skill 不会在搜索阶段直接塞进上下文。

### 第 2 阶段：提升检索质量

- 增加同义词表和关键词切分。
- 建立统一 `search_context`。
- 为资源补齐 frontmatter 或 manifest。
- 加入资源风险等级和默认启用开关。

验收标准：

- `架构设计` 能同时召回架构 prompt、架构模板文档、相关 skill。
- `前端` 能召回前端 prompt 和未来的 frontend skill。
- 搜索结果解释命中原因。

### 第 3 阶段：补齐工作流

- 实现 `recommend_workflow`。
- 实现 `generate_plan_doc` 和 `generate_architecture_doc`。
- 实现 `generate_agent_rules`。
- 新增 `project-planning`、`context-engineering`、`code-review`、
  `debugging`、`testing` 五个基础 skills。

验收标准：

- 用户输入一句需求后，MCP 能推荐“用哪些资源 + 产出什么文档 + 下一步怎么做”。
- AI 不只是搜索资料，而是能形成完整开发闭环。

### 第 4 阶段：资源同步和质量门禁

- 新增资源同步脚本。
- 新增资源审查脚本。
- 测试中加入资源数量、敏感资源、超大资源、frontmatter 完整性检查。
- README/USAGE 与实际能力保持一致。

验收标准：

- 主仓资源更新后，一条命令同步到 MCP。
- 不合格资源不会进入默认索引。
- 文档声明与实际工具能力一致。

## 当前验证记录

- 已确认 `vibe-code-mcp` 是嵌套 Git 仓库，外层工作区不是 Git 仓库。
- 已确认中文资源数量：47 prompts、14 skills、17 docs。
- 已确认主仓 `i18n/zh` 与 MCP `data/i18n/zh` 的 prompts、skills、docs 数量一致。
- 已确认 skill references 数量一致：92。
- 已确认 skill scripts 数量一致：4。
- 当前环境缺少 `pyyaml`，直接加载 `config.yaml` 会失败。
- 当前环境缺少 `pytest`，无法运行 README 声称的测试命令。

## 总体判断

`vibe-code-mcp` 当前适合作为 MVP，但还不适合作为长期高效的 AI
编程上下文系统。下一步不建议单纯继续堆更多长 prompt 和 skill，
而应优先改造工具协议和资源索引方式：

1. 搜索只给摘要。
2. 精确读取才给正文。
3. 用工作流工具连接 prompts、skills、docs。
4. 用资源 manifest 管理质量、风险和适用场景。
5. 再补齐通用软件工程 skills。

这样才能真正达到“好用、省 token、让 AI 工作更完整”的目标。
