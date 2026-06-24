---
name: mcp-development
description: "MCP 开发技能：设计、实现、测试和调试 Model Context Protocol Server。Use when building MCP tools/resources/prompts, Python MCP server, stdio/SSE transports, tool schema, MCP integration."
---

# MCP Development

用于构建生产可用的 MCP Server，让 AI 助手安全、稳定地访问外部能力。

## 使用场景

- 创建 Python 或 TypeScript MCP Server。
- 设计 tools、resources、prompts 的边界。
- 编写 tool schema、错误处理、权限控制和测试。
- 调试 stdio、SSE、Streamable HTTP 或客户端集成问题。
- 优化当前 `vibe-code-mcp` 的工具粒度和资源读取方式。

## MCP 原语选择

- Tool：执行动作，可能有副作用，例如搜索、写文件、创建 issue。
- Resource：只读数据源，用 URI 标识，例如 `docs://id`。
- Prompt：预定义交互模板，用来启动工作流。

选择原则：

- 需要模型主动调用并执行操作：Tool。
- 需要按 URI 读取数据：Resource。
- 需要引导用户或模型进入流程：Prompt。

## Tool 设计检查

1. 名称用动词开头，snake_case。
2. 描述写清用途、返回内容、限制和副作用。
3. 参数有类型、默认值、枚举和说明。
4. 输出结构稳定，错误也用结构化 JSON 或 Markdown。
5. 外部调用设置超时和异常处理。
6. 危险操作拆成预览和确认两步。
7. 每个 tool 有正常、错误、边界测试。

## 当前 MCP 优化建议

对 `vibe-code-mcp`：

- 搜索工具默认返回 metadata。
- 增加 `get_resource` 按 id 读取正文。
- 增加 `list_skill_references` 和 `get_skill_reference`。
- 增加 `search_context` 聚合 prompts、skills、docs。
- 为资源增加风险等级、默认启用状态、来源和 token 估算。

## 参考资料

- `references/server-design.md`：MCP Server 结构和工具设计。
- `references/testing-debugging.md`：测试、Inspector 和调试。
- `references/source-map.md`：来源与许可证。
