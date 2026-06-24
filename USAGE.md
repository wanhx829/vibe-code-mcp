# Vibe Code MCP Server 详细使用手册

> 本手册详细介绍如何安装、配置和使用 Vibe Code MCP Server，以及如何通过它提升 AI 编程效率。

---

## 目录

1. [项目简介](#1-项目简介)
2. [核心价值](#2-核心价值)
3. [系统要求](#3-系统要求)
4. [安装指南](#4-安装指南)
5. [配置说明](#5-配置说明)
6. [CLI 集成](#6-claude-cli-集成)
   - [6.5 MCP Server 工作原理](#65-mcp-server-工作原理)
   - [6.6 Codex CLI 集成](#66-codex-cli-集成)
7. [工具详细说明](#7-工具详细说明)
8. [使用场景与示例](#8-使用场景与示例)
9. [工作流最佳实践](#9-工作流最佳实践)
10. [故障排除](#10-故障排除)
11. [高级配置](#11-高级配置)
12. [开发指南](#12-开发指南)

---

## 1. 项目简介

Vibe Code MCP Server 是一个基于 MCP（Model Context Protocol）协议的服务器，将内置的 AI 编程提示词库、技能库、方法论文档和模板资源暴露为结构化工具，供 Claude CLI 调用。

### 1.1 什么是 MCP？

MCP（Model Context Protocol）是一种标准化协议，允许 AI 助手（如 Claude）与外部工具和数据源进行交互。通过 MCP Server，Claude 可以：

- 访问本地文件和数据库
- 调用自定义工具和 API
- 获取实时信息和上下文

### 1.2 项目包含的资源

| 资源类型 | 数量 | 说明 |
|----------|------|------|
| 提示词 | 47 | 编程、系统、用户、元提示词等分类 |
| 技能 | 22 | PostgreSQL、Agent、MCP、RAG、代码审查等专业领域 |
| 文档 | 17 | 方法论、模板、教程等 |
| 模板 | 1 | 项目上下文文档模板 |

---

## 2. 核心价值

### 2.1 解决的问题

**传统方式的痛点**：
- 需要手动复制粘贴提示词
- 难以记住所有可用的技能和资源
- 缺乏结构化的项目文档模板
- 跨项目无法共享最佳实践

**MCP Server 的解决方案**：
- Claude 自动选择最合适的工具和资源
- 一键搜索和调用，无需手动查找
- 标准化的项目文档生成
- 统一的资源管理，跨项目共享

### 2.2 效率提升

**Before（传统方式）**：
```
用户：帮我写一个 PostgreSQL 数据库设计
Claude：好的，请告诉我你的需求...
用户：（手动复制粘贴相关提示词）
Claude：（基于有限上下文生成代码）
```

**After（使用 MCP Server）**：
```
用户：帮我写一个 PostgreSQL 数据库设计
Claude：（自动调用 search_skills 查询 PostgreSQL 技能）
       （自动调用 search_prompts 查询数据库设计提示词）
       （基于完整上下文生成高质量代码）
```

### 2.3 适用人群

- **AI 编程用户**：使用 Claude CLI 进行日常开发
- **团队开发者**：需要统一的开发规范和最佳实践
- **技术管理者**：需要标准化项目文档和流程
- **学习者**：希望获取专业的编程知识和技能

---

## 3. 系统要求

### 3.1 必需环境

| 组件 | 版本要求 | 说明 |
|------|----------|------|
| Python | 3.10+ | 推荐 3.11 或更高版本 |
| Claude CLI | 最新版 | 支持 MCP 协议的版本 |
| 操作系统 | Windows/macOS/Linux | 跨平台支持 |

### 3.2 Python 依赖

```
mcp>=1.0.0
pyyaml>=6.0
```

### 3.3 网络要求

- 无需网络连接（本地运行）
- 无需外部数据库
- 无需 API 密钥

---

## 4. 安装指南

### 4.1 下载项目

```bash
# 方式 1：克隆仓库（推荐）
git clone https://github.com/YOUR_USERNAME/vibe-code-mcp.git
cd vibe-code-mcp

# 方式 2：直接下载
# 下载 ZIP 文件并解压
```

### 4.2 安装依赖

```bash
cd vibe-code-mcp
pip install -r requirements.txt
```

**验证安装**：
```bash
python -c "import mcp; import yaml; print('依赖安装成功')"
```

### 4.3 验证安装

```bash
# 运行测试
pip install -r requirements-dev.txt
python -m pytest tests/ -v

# 预期输出：43 个测试全部通过
```

### 4.4 测试启动

```bash
python server.py
```

预期输出（stderr）：
```
Vibe Coding MCP Server 启动完成: 47 提示词, 22 技能, 17 文档
```

按 `Ctrl+C` 退出。

---

## 5. 配置说明

### 5.1 配置文件结构

`config.yaml` 包含以下配置项：

```yaml
# 资源目录路径（相对于 config.yaml 文件位置）
resource_path: "./data"

# 默认语言
default_language: "zh"

# 服务器配置
server:
  name: "vibe-code-mcp"  # 服务器名称
  version: "1.0.0"       # 版本号

# 扫描配置
scan:
  include_prompt_docs: false   # 不包含外部提示词库
  max_summary_length: 500      # 摘要最大长度
  languages: ["zh"]            # 扫描的语言列表
```

### 5.2 配置项详解

#### resource_path

**作用**：指定资源目录路径

**示例**：
```yaml
# 相对路径（相对于 config.yaml 文件位置）
resource_path: "./data"

# 绝对路径
resource_path: "D:/path/to/vibe-code-mcp/data"
```

**注意事项**：
- 支持相对路径和绝对路径
- 相对路径相对于 config.yaml 文件位置
- 使用正斜杠 `/` 或双反斜杠 `\\`
- 支持中文路径

#### default_language

**作用**：设置默认语言

**可选值**：
- `"zh"` - 中文（默认）

#### scan.include_prompt_docs

**作用**：是否扫描外部提示词库

**可选值**：
- `false` - 不包含外部提示词库（默认）
- `true` - 包含 `libs/external/prompts-library/prompt_docs/` 目录

**建议**：通常设为 `false`，使用内置资源即可

#### scan.languages

**作用**：指定扫描哪些语言的资源

**示例**：
```yaml
# 只扫描中文
languages: ["zh"]
```

### 5.3 环境变量

可以通过环境变量 `VIBE_CONFIG` 指定配置文件路径：

```bash
# Windows
set VIBE_CONFIG=D:\path\to\vibe-code-mcp\config.yaml

# macOS/Linux
export VIBE_CONFIG=/path/to/vibe-code-mcp/config.yaml

# 启动服务器
python server.py
```

---

## 6. Claude CLI 集成

### 6.1 配置方式

有两种配置方式：

#### 方式 1：用户级配置（推荐）

编辑 `~/.claude/settings.json` 文件：

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

**配置说明**：
- `command`：Python 解释器路径
- `args`：server.py 的绝对路径
- `env.VIBE_CONFIG`：配置文件的绝对路径

#### 方式 2：项目级配置

在项目根目录创建 `.claude/settings.json`，内容同上。

**适用场景**：不同项目使用不同的 MCP Server 配置

### 6.2 配置文件位置

| 操作系统 | 配置文件路径 |
|----------|--------------|
| Windows | `C:\Users\USERNAME\.claude\settings.json` |
| macOS | `/Users/USERNAME/.claude/settings.json` |
| Linux | `/home/USERNAME/.claude/settings.json` |

### 6.3 验证集成

1. **重启 Claude CLI**（必须）

2. **测试工具调用**：

```
帮我搜索架构设计相关的提示词
```

Claude 应自动调用 `search_prompts` 工具并返回结果。

3. **查看工具列表**：

```
你有哪些可用的工具？
```

Claude 应列出 4 个 MCP 工具。

### 6.4 多个 MCP Server

可以同时配置多个 MCP Server：

```json
{
  "mcpServers": {
    "vibe-code-mcp": {
      "command": "python",
      "args": ["D:/path/to/vibe-code-mcp/server.py"],
      "env": {
        "VIBE_CONFIG": "D:/path/to/vibe-code-mcp/config.yaml"
      }
    },
    "another-mcp": {
      "command": "python",
      "args": ["D:/path/to/another/server.py"]
    }
  }
}
```

---

## 6.5 MCP Server 工作原理

### 是否需要手动启动 Server？

**不需要**。Claude CLI 会自动管理 MCP Server 的生命周期。

### 工作流程

```
┌─────────────────────────────────────────────────────────────┐
│                     Claude CLI                              │
│  1. 读取 ~/.claude/settings.json 配置                       │
│  2. 自动启动 MCP Server 子进程                              │
│  3. 通过 stdin/stdout 与 Server 通信 (MCP 协议)             │
│  4. 用户提问时自动调用 MCP 工具                              │
│  5. 退出时自动关闭 Server 进程                               │
└─────────────────────────────────────────────────────────────┘
```

### 关键特性

| 特性 | 说明 |
|------|------|
| 自动启动 | Claude CLI 启动时自动启动 MCP Server |
| 自动停止 | Claude CLI 退出时自动关闭 Server |
| 进程管理 | Server 是 Claude CLI 的子进程，无需手动管理 |
| 通信方式 | stdio（标准输入输出），不是 HTTP 服务 |
| 多实例 | 每次启动 Claude CLI 都会创建新的 Server 实例 |

### 使用流程

1. **一次性配置**：编辑 `~/.claude/settings.json` 添加 MCP Server
2. **启动 Claude CLI**：直接运行 `claude` 命令
3. **直接对话**：无需任何额外操作，直接提问即可

```
用户：帮我搜索架构设计相关的提示词
Claude：（自动调用 search_prompts 工具）
       找到以下相关提示词...
```

### 常见误解

- **误解**：需要先运行 `python server.py` 启动服务
- **正确**：无需手动启动，Claude CLI 会自动处理

### 配置中为什么用 command + args 而不是端口？

MCP Server 使用 **stdio 传输**（标准输入输出），不是 HTTP 服务：

```json
{
  "command": "python",           // 启动命令
  "args": ["server.py"],        // 命令参数
  "env": { ... }                // 环境变量
}
```

这与 HTTP 服务不同：
- HTTP 服务：需要先启动，监听端口，然后客户端连接
- MCP Server：由 Claude CLI 直接启动子进程，通过管道通信

---

## 6.6 Codex CLI 集成

### 配置方式

Codex CLI 使用 TOML 格式的配置文件。

#### 用户级配置（推荐）

编辑 `~/.codex/config.toml` 文件：

```toml
[mcp_servers.vibe-code-mcp]
command = "python"
args = ["D:/path/to/vibe-code-mcp/server.py"]

[mcp_servers.vibe-code-mcp.env]
VIBE_CONFIG = "D:/path/to/vibe-code-mcp/config.yaml"
```

**配置说明**：
- `command`：Python 解释器路径
- `args`：server.py 的绝对路径
- `env.VIBE_CONFIG`：配置文件的绝对路径

#### 项目级配置

在项目根目录创建 `codex.toml`，内容同上。

**适用场景**：不同项目使用不同的 MCP Server 配置

### 配置文件位置

| 操作系统 | 配置文件路径 |
|----------|--------------|
| Windows | `C:\Users\USERNAME\.codex\config.toml` |
| macOS | `/Users/USERNAME/.codex/config.toml` |
| Linux | `/home/USERNAME/.codex/config.toml` |

### 验证集成

1. **重启 Codex CLI**（必须）

2. **测试工具调用**：

```
帮我搜索架构设计相关的提示词
```

Codex 应自动调用 `search_prompts` 工具并返回结果。

3. **查看工具列表**：

```
你有哪些可用的工具？
```

Codex 应列出 4 个 MCP 工具。

### 多个 MCP Server

可以同时配置多个 MCP Server：

```toml
[mcp_servers.vibe-code-mcp]
command = "python"
args = ["D:/path/to/vibe-code-mcp/server.py"]

[mcp_servers.vibe-code-mcp.env]
VIBE_CONFIG = "D:/path/to/vibe-code-mcp/config.yaml"

[mcp_servers.another-mcp]
command = "python"
args = ["D:/path/to/another/server.py"]
```

---

## 7. 工具详细说明

### 7.1 search_prompts

**功能**：搜索 AI 编程提示词库

**使用场景**：
- 需要特定编程任务的提示词
- 寻找代码生成的最佳实践
- 查找调试和优化建议

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| query | string | 是 | - | 搜索关键词或需求描述 |
| category | string | 否 | "all" | 提示词分类 |
| language | string | 否 | "zh" | 语言 |

**category 可选值**：
- `coding` - 编程类提示词
- `system` - 系统类提示词
- `user` - 用户类提示词
- `meta` - 元提示词
- `all` - 所有分类（默认）

**返回字段**：
```json
{
  "id": "coding_zh_(1,1)_项目上下文与代码审查.md",
  "title": "项目上下文与代码审查",
  "path": "D:/path/to/vibe-code-mcp/data/i18n/zh/prompts/coding_prompts/(1,1)_项目上下文与代码审查.md",
  "category": "coding",
  "language": "zh",
  "tags": ["编程", "项目", "上下文", "代码审查"],
  "summary": "将自然语言需求转换为结构化项目上下文文档...",
  "content": "# 项目上下文与代码审查\n\n...",
  "size": 1234
}
```

**搜索权重**：
- 标题匹配：+3
- 标签匹配：+2
- 摘要匹配：+1

### 7.2 search_skills

**功能**：查询 AI 技能库

**使用场景**：
- 需要特定领域的专业知识
- 寻找技术栈的最佳实践
- 获取专业工具的使用指南

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| keyword | string | 是 | - | 技能关键词 |
| language | string | 否 | "zh" | 语言 |

**可用技能示例**：
- `postgresql` - PostgreSQL 数据库
- `ccxt` - 加密货币交易所 API
- `telegram` - Telegram Bot 开发
- `claude` - Claude 使用技巧

**返回字段**：
```json
{
  "id": "postgresql",
  "title": "PostgreSQL 专家",
  "path": "D:/path/to/vibe-code-mcp/data/i18n/zh/skills/postgresql/SKILL.md",
  "domain": "PostgreSQL 数据库最佳实践",
  "language": "zh",
  "size": 76000,
  "content": "---\nname: postgresql\n...",
  "references": [
    {
      "title": "cli",
      "path": "D:/path/to/vibe-code-mcp/data/i18n/zh/skills/postgresql/references/cli.md"
    }
  ]
}
```

**搜索权重**：
- ID 匹配：+3
- 标题匹配：+3
- 领域描述匹配：+2
- 内容匹配：+1

### 7.3 search_docs

**功能**：检索方法论、经验总结和模板资源

**使用场景**：
- 寻找编程方法论和最佳实践
- 获取项目模板和架构设计
- 学习开发经验和技巧

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| topic | string | 是 | - | 搜索主题 |
| doc_type | string | 否 | "all" | 文档类型 |
| language | string | 否 | "zh" | 语言 |

**doc_type 可选值**：
- `methodology` - 方法论
- `template` - 模板
- `tutorial` - 教程
- `all` - 所有类型（默认）

**返回字段**：
```json
{
  "id": "methodology_zh_开发经验.md",
  "title": "开发经验",
  "path": "D:/path/to/vibe-code-mcp/data/i18n/zh/documents/Methodology and Principles/开发经验.md",
  "type": "methodology",
  "language": "zh",
  "tags": ["方法论", "开发", "经验"],
  "summary": "变量命名、文件结构、编码规范、架构原则等实践经验...",
  "content": "# 开发经验\n\n...",
  "size": 5678
}
```

**搜索权重**：
- 标题匹配：+3
- 标签匹配：+2
- 摘要匹配：+1
- 内容匹配：+1

### 7.4 generate_project_doc

**功能**：生成标准化项目文档

**使用场景**：
- 启动新项目时创建项目文档
- 规范化项目上下文和需求
- 生成技术文档模板

**参数**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| doc_type | string | 是 | - | 文档类型 |
| project_name | string | 是 | - | 项目名称 |
| project_desc | string | 是 | - | 项目简要描述 |
| tech_stack | string | 否 | "" | 技术栈 |

**doc_type 可选值**：
- `context` - 项目上下文文档

**返回字段**：
```json
{
  "content": "# 我的项目 项目上下文文档\n\n## 项目概要\n\n...",
  "doc_type": "context"
}
```

**生成的文档包含**：
- 项目概要
- 项目背景
- 技术栈
- 架构设计
- 功能需求
- 非功能需求
- 开发规范
- 里程碑

---

## 8. 使用场景与示例

### 8.1 场景 1：新项目启动

**需求**：创建一个新的 Web 项目

**对话示例**：
```
用户：我要创建一个电商网站，使用 React + Node.js + PostgreSQL

Claude：（自动调用 generate_project_doc 生成项目文档）
       （自动调用 search_skills 查询 PostgreSQL 技能）
       （自动调用 search_prompts 查询 Web 开发提示词）

       好的，我为你生成了项目文档，并找到了相关的技能和提示词。
       基于这些资源，我建议...
```

### 8.2 场景 2：代码审查

**需求**：审查现有代码的质量

**对话示例**：
```
用户：帮我审查这段代码的质量

Claude：（自动调用 search_prompts 查询代码审查提示词）
       （自动调用 search_docs 查询编码规范文档）

       好的，我找到了代码审查的最佳实践。
       基于这些规范，我建议...
```

### 8.3 场景 3：技术选型

**需求**：选择合适的数据库

**对话示例**：
```
用户：我应该选择 MongoDB 还是 PostgreSQL？

Claude：（自动调用 search_skills 查询数据库技能）
       （自动调用 search_docs 查询数据库设计文档）

       好的，我找到了数据库选型的相关资料。
       基于你的需求，我建议...
```

### 8.4 场景 4：学习新技术

**需求**：学习 PostgreSQL

**对话示例**：
```
用户：我想学习 PostgreSQL，有什么建议？

Claude：（自动调用 search_skills 查询 PostgreSQL 技能）
       （自动调用 search_docs 查询学习教程）

       好的，我找到了 PostgreSQL 的完整学习资料。
       我建议你从...
```

### 8.5 场景 5：调试问题

**需求**：解决数据库连接问题

**对话示例**：
```
用户：我的 PostgreSQL 连接失败了

Claude：（自动调用 search_skills 查询 PostgreSQL 技能）
       （自动调用 search_prompts 查询调试提示词）

       好的，我找到了 PostgreSQL 连接问题的解决方案。
       请检查...
```

---

## 9. 工作流最佳实践

### 9.1 项目启动工作流

1. **生成项目文档**
   ```
   帮我生成一个项目文档，项目名是"电商系统"，描述是"一个现代化的电商平台"
   ```

2. **查询相关技能**
   ```
   查询 PostgreSQL 和 React 相关的技能
   ```

3. **获取最佳实践**
   ```
   搜索 Web 开发的最佳实践
   ```

4. **开始开发**
   ```
   基于这些资料，帮我设计数据库架构
   ```

### 9.2 代码审查工作流

1. **获取审查标准**
   ```
   搜索代码审查的提示词和规范
   ```

2. **执行审查**
   ```
   帮我审查这段代码
   ```

3. **获取改进建议**
   ```
   搜索代码优化的最佳实践
   ```

### 9.3 学习工作流

1. **获取学习资料**
   ```
   查询 PostgreSQL 相关的技能和教程
   ```

2. **获取实践指南**
   ```
   搜索数据库设计的模板和示例
   ```

3. **开始实践**
   ```
   帮我设计一个数据库
   ```

### 9.4 调试工作流

1. **获取调试指南**
   ```
   搜索数据库调试的提示词
   ```

2. **查询专业知识**
   ```
   查询 PostgreSQL 的错误处理技能
   ```

3. **解决问题**
   ```
   帮我解决这个连接问题
   ```

---

## 10. 故障排除

### 10.1 常见问题

#### 问题 1：MCP Server 启动失败

**错误信息**：
```
配置加载失败: Config file not found: config.yaml
```

**解决方案**：
1. 检查 `config.yaml` 文件是否存在
2. 检查文件路径是否正确
3. 使用环境变量指定配置文件路径

#### 问题 2：资源路径不存在

**错误信息**：
```
resource_path does not exist: ./data
```

**解决方案**：
1. 检查 `data` 目录是否存在
2. 检查路径是否正确（使用正斜杠）
3. 确保目录结构完整

#### 问题 3：Claude 无法调用工具

**现象**：Claude 没有调用 MCP 工具

**解决方案**：
1. 重启 Claude CLI（必须）
2. 检查 `~/.claude/settings.json` 配置是否正确
3. 检查 Python 路径是否正确
4. 查看 Claude CLI 日志

#### 问题 4：搜索结果为空

**现象**：搜索返回空结果

**解决方案**：
1. 检查资源目录是否有内容
2. 尝试不同的搜索关键词
3. 检查语言配置是否正确

#### 问题 5：测试失败

**错误信息**：
```
FAILED tests/test_xxx.py::test_xxx
```

**解决方案**：
1. 检查依赖是否安装完整：`pip install -r requirements-dev.txt`
2. 检查 Python 版本是否符合要求
3. 查看详细错误信息

### 10.2 调试技巧

#### 查看服务器日志

```bash
python server.py 2> server.log
```

#### 测试配置加载

```python
from resources.config import load_config
config = load_config("config.yaml")
print(config)
```

#### 测试资源扫描

```python
from resources.prompt_loader import PromptLoader
loader = PromptLoader("./data")
loader.scan()
print(f"找到 {len(loader.prompts)} 个提示词")
```

### 10.3 获取帮助

如果问题仍未解决：

1. 查看 `MCP-GENERATION-GUIDE.md` 文档
2. 检查 GitHub Issues
3. 提交新的 Issue，包含：
   - 错误信息
   - 操作系统和 Python 版本
   - 配置文件内容
   - 重现步骤

---

## 11. 高级配置

### 11.1 自定义搜索权重

修改 `resources/` 目录下对应 loader 的 `search` 方法：

```python
# 提示词搜索权重（默认）
if query_lower in entry["title"].lower():
    score += 3  # 标题匹配
if any(query_lower in tag.lower() for tag in entry["tags"]):
    score += 2  # 标签匹配
if query_lower in entry["summary"].lower():
    score += 1  # 摘要匹配
```

### 11.2 添加新工具

1. 在 `tools/` 目录创建新文件
2. 实现 `handle` 异步函数
3. 在 `server.py` 的 `list_tools` 和 `call_tool` 中注册
4. 添加对应测试

### 11.3 添加新资源类型

1. 在 `resources/` 目录创建新 loader
2. 实现 `scan` 和 `search` 方法
3. 在 `server.py` 中初始化和调用
4. 添加对应工具

### 11.4 性能优化

#### 减少扫描范围

```yaml
scan:
  languages: ["zh"]  # 只扫描中文
  include_prompt_docs: false  # 不包含外部提示词库
```

#### 使用缓存

loader 会缓存扫描结果，重启服务器才会更新。

### 11.5 多环境配置

创建多个配置文件：

```bash
# 开发环境
config.dev.yaml

# 生产环境
config.prod.yaml

# 测试环境
config.test.yaml
```

使用环境变量指定：

```bash
set VIBE_CONFIG=config.dev.yaml
python server.py
```

---

## 12. 开发指南

### 12.1 开发环境设置

```bash
# 克隆仓库
git clone https://github.com/YOUR_USERNAME/vibe-code-mcp.git
cd vibe-code-mcp/mcp-server

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements-dev.txt
```

### 12.2 运行测试

```bash
# 运行所有测试
python -m pytest tests/ -v

# 运行特定测试
python -m pytest tests/test_config.py -v

# 运行并显示覆盖率
pip install pytest-cov
python -m pytest tests/ --cov=resources --cov=tools
```

### 12.3 代码规范

- 使用 Python 3.10+ 语法
- 遵循 PEP 8 规范
- 添加类型注解
- 编写文档字符串

### 12.4 提交规范

```
feat: 添加新功能
fix: 修复 bug
docs: 更新文档
test: 添加测试
refactor: 重构代码
```

### 12.5 发布流程

1. 更新版本号（`config.yaml`）
2. 更新 `README.md` 和 `USAGE.md`
3. 运行测试确保通过
4. 提交代码
5. 创建 GitHub Release

---

## 附录 A：资源目录结构

```
vibe-code-mcp/
├── data/
│   └── i18n/
│       └── zh/
│           ├── prompts/
│           │   ├── coding_prompts/       # 编程类提示词
│           │   ├── system_prompts/       # 系统类提示词
│           │   ├── user_prompts/         # 用户类提示词
│           │   └── meta_prompts/         # 元提示词
│           ├── skills/
│           │   └── <skill_name>/
│           │       ├── SKILL.md          # 技能定义
│           │       └── references/       # 参考文档
│           └── documents/
│               ├── Methodology and Principles/   # 方法论
│               ├── Templates and Resources/      # 模板
│               └── Tutorials and Guides/         # 教程
├── resources/                         # Python 模块
├── tools/                             # MCP 工具
├── templates/                         # 文档模板
└── tests/                             # 测试
```

## 附录 B：MCP 工具参数速查

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

## 附录 C：常见问题快速解答

| 问题 | 解决方案 |
|------|----------|
| MCP Server 启动失败 | 检查 config.yaml 路径和资源目录 |
| Claude 无法调用工具 | 重启 Claude CLI，检查 settings.json |
| 搜索结果为空 | 检查资源目录，尝试不同关键词 |
| 测试失败 | 安装 dev 依赖，检查 Python 版本 |
| 中文乱码 | 确保文件编码为 UTF-8 |

---

**最后更新**：2026-06-23

**版本**：1.0.0

**作者**：Vibe Coding Team
