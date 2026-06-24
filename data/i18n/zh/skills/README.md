# 🎯 AI Skills 技能库

`i18n/zh/skills/` 目录存放 AI 技能（Skills），这些是比提示词更高级的能力封装，可以让 AI 在特定领域表现出专家级水平。当前包含 **22 个**专业技能。

## 目录结构

```
i18n/zh/skills/
├── README.md                # 本文件
│
├── # === 元技能（核心） ===
├── claude-skills/           # ⭐ 元技能：生成 Skills 的 Skills（11KB）
│
├── # === AI 编程与 Agent 工程 ===
├── agent-engineering/        # Agent 架构、工具、记忆、评估
├── context-engineering/      # 上下文选择、压缩、记忆、长任务维护
├── mcp-development/          # MCP Server 设计、工具 schema、调试
├── prompt-engineering/       # Prompt 设计、优化、评估
├── rag-development/          # RAG 检索、分块、引用、评估
├── llm-app-development/      # LLM 应用架构、工具调用、运维
├── code-review/              # 代码审查、风险分级、中文 review 表达
├── debugging/                # 系统化调试、根因定位、验证
│
├── # === Claude 工具 ===
├── claude-code-guide/       # Claude Code 使用指南（9KB）
├── claude-cookbooks/        # Claude API 最佳实践（9KB）
│
├── # === 数据库 ===
├── postgresql/              # ⭐ PostgreSQL 专家技能（76KB，最详细）
├── timescaledb/             # 时序数据库扩展（3KB）
│
├── # === 加密货币/量化 ===
├── ccxt/                    # 加密货币交易所统一 API（18KB）
├── coingecko/               # CoinGecko 行情 API（3KB）
├── cryptofeed/              # 加密货币实时数据流（6KB）
├── hummingbot/              # 量化交易机器人框架（4KB）
├── polymarket/              # 预测市场 API（6KB）
│
├── # === 开发工具 ===
├── telegram-dev/            # Telegram Bot 开发（18KB）
├── twscrape/                # Twitter/X 数据抓取（11KB）
├── snapdom/                 # DOM 快照工具（8KB）
└── proxychains/             # 代理链配置（6KB）
```

## Skills 一览表

### 按文件大小排序（详细程度）

| 技能 | 大小 | 领域 | 说明 |
|------|------|------|------|
| **postgresql** | 76KB | 数据库 | ⭐ 最详细，PostgreSQL 完整专家技能 |
| **telegram-dev** | 18KB | Bot 开发 | Telegram Bot 开发完整指南 |
| **ccxt** | 18KB | 交易 | 加密货币交易所统一 API |
| **twscrape** | 11KB | 数据采集 | Twitter/X 数据抓取 |
| **claude-skills** | 11KB | 元技能 | ⭐ 生成 Skills 的 Skills |
| **claude-code-guide** | 9KB | 工具 | Claude Code 使用最佳实践 |
| **claude-cookbooks** | 9KB | 工具 | Claude API 使用示例 |
| **snapdom** | 8KB | 前端 | DOM 快照与测试 |
| **cryptofeed** | 6KB | 数据流 | 加密货币实时数据流 |
| **polymarket** | 6KB | 预测市场 | Polymarket API 集成 |
| **proxychains** | 6KB | 网络 | 代理链配置与使用 |
| **hummingbot** | 4KB | 量化 | 量化交易机器人框架 |
| **timescaledb** | 3KB | 数据库 | PostgreSQL 时序扩展 |
| **coingecko** | 3KB | 行情 | CoinGecko 行情 API |

### 按领域分类

#### 🔧 元技能与工具

| 技能 | 说明 | 推荐场景 |
|------|------|----------|
| `claude-skills` | 生成 Skills 的 Skills | 创建新技能时必用 |
| `claude-code-guide` | Claude Code CLI 使用指南 | 日常开发 |
| `claude-cookbooks` | Claude API 最佳实践 | API 集成 |

#### 🗄️ 数据库

| 技能 | 说明 | 推荐场景 |
|------|------|----------|
| `postgresql` | PostgreSQL 完整指南（76KB） | 关系型数据库开发 |
| `timescaledb` | 时序数据库扩展 | 时间序列数据 |

#### 💰 加密货币/量化

| 技能 | 说明 | 推荐场景 |
|------|------|----------|
| `ccxt` | 交易所统一 API | 多交易所对接 |
| `coingecko` | 行情数据 API | 价格查询 |
| `cryptofeed` | 实时数据流 | WebSocket 行情 |
| `hummingbot` | 量化交易框架 | 自动化交易 |
| `polymarket` | 预测市场 API | 预测市场交易 |

#### 🛠️ 开发工具

| 技能 | 说明 | 推荐场景 |
|------|------|----------|
| `telegram-dev` | Telegram Bot 开发 | Bot 开发 |
| `twscrape` | Twitter 数据抓取 | 社交媒体数据 |
| `snapdom` | DOM 快照 | 前端测试 |
| `proxychains` | 代理链配置 | 网络代理 |

## Skills vs Prompts 的区别

| 维度 | Prompts（提示词） | Skills（技能） |
|------|------------------|----------------|
| 粒度 | 单次任务指令 | 完整能力封装 |
| 复用性 | 复制粘贴 | 配置后自动生效 |
| 上下文 | 需手动提供 | 内置领域知识 |
| 适用场景 | 临时任务 | 长期项目 |
| 结构 | 单文件 | 目录（含 assets/scripts/references） |

## 技能目录结构

每个技能遵循统一结构：

```
skill-name/
├── SKILL.md         # 技能主文件，包含领域知识和规则
├── assets/          # 静态资源（图片、配置模板等）
├── scripts/         # 辅助脚本
└── references/      # 参考文档
```

## 快速使用

### 1. 查看技能

```bash
# 查看元技能
cat i18n/zh/skills/claude-skills/SKILL.md

# 查看 PostgreSQL 技能（最详细）
cat i18n/zh/skills/postgresql/SKILL.md

# 查看 Telegram Bot 开发技能
cat i18n/zh/skills/telegram-dev/SKILL.md
```

### 2. 复制到项目中使用

```bash
# 复制整个技能目录
cp -r i18n/zh/skills/postgresql/ ./my-project/

# 或只复制主文件到 CLAUDE.md
cp i18n/zh/skills/postgresql/SKILL.md ./CLAUDE.md
```

### 3. 结合 Claude Code 使用

在项目根目录创建 `CLAUDE.md`，引用技能：

```markdown
# 项目规则

请参考以下技能文件：
@i18n/zh/skills/postgresql/SKILL.md
@i18n/zh/skills/telegram-dev/SKILL.md
```

## 创建自定义 Skill

### 方法一：使用元技能生成（推荐）

1. 准备领域资料（文档、代码、规范）
2. 将资料和 `i18n/zh/skills/claude-skills/SKILL.md` 一起提供给 AI
3. AI 会生成针对该领域的专用 Skill

```bash
# 示例：让 AI 读取元技能后生成新技能
cat i18n/zh/skills/claude-skills/SKILL.md
# 然后告诉 AI：请根据这个元技能，为 [你的领域] 生成一个新的 SKILL.md
```

### 方法二：手动创建

```bash
# 创建技能目录
mkdir -p i18n/zh/skills/my-skill/{assets,scripts,references}

# 创建主文件
cat > i18n/zh/skills/my-skill/SKILL.md << 'EOF'
# My Skill

## 概述
简要说明技能用途和适用场景

## 领域知识
- 核心概念
- 最佳实践
- 常见模式

## 规则与约束
- 必须遵守的规则
- 禁止的操作
- 边界条件

## 示例
具体的使用示例和代码片段

## 常见问题
FAQ 和解决方案
EOF
```

## 核心技能详解

### `claude-skills/SKILL.md` - 元技能 ⭐

**生成 Skills 的 Skills**，是创建新技能的核心工具。

使用方法：
1. 准备你的领域资料（文档、代码、规范等）
2. 将资料和 SKILL.md 一起提供给 AI
3. AI 会生成针对该领域的专用 Skill

### `postgresql/SKILL.md` - PostgreSQL 专家 ⭐

最详细的技能（76KB），包含：
- 数据库设计最佳实践
- 查询优化技巧
- 索引策略
- 性能调优
- 常见问题解决方案
- SQL 代码示例

### `telegram-dev/SKILL.md` - Telegram Bot 开发

完整的 Telegram Bot 开发指南（18KB）：
- Bot API 使用
- 消息处理
- 键盘与回调
- Webhook 配置
- 错误处理

### `ccxt/SKILL.md` - 加密货币交易所 API

统一的交易所 API 封装（18KB）：
- 支持 100+ 交易所
- 统一的数据格式
- 订单管理
- 行情获取

## 相关资源

- [Skills 生成器](https://github.com/yusufkaraaslan/Skill_Seekers) - 把任何资料转为 AI Skills
- [元技能文件](./claude-skills/SKILL.md) - 生成 Skills 的 Skills
- [提示词库](../prompts/) - 更细粒度的提示词集合
- [Claude Code 指南](./claude-code-guide/SKILL.md) - Claude Code 使用最佳实践
- [文档库](../documents/) - 方法论与开发经验
