# MCP Server 设计

## 推荐结构

```text
mcp-server/
|-- server.py
|-- resources/
|-- tools/
|-- templates/
|-- tests/
`-- config.yaml
```

## Tool schema

每个 tool 的 schema 应该让模型能独立判断：

- 什么时候调用。
- 必填参数是什么。
- 参数有什么取值范围。
- 返回值能用于什么下一步。
- 是否有副作用。

## 错误处理

错误信息要可操作：

- 参数错误：指出缺少或非法字段。
- 权限不足：说明需要什么权限。
- 资源不存在：返回可选的搜索建议。
- 外部服务失败：返回重试建议和失败摘要。

不要让异常冒泡导致 MCP Server 退出。

## Resources 与 Prompts

Resources 适合只读知识库。Prompts 适合固定流程入口。

对于资源型 MCP：

- 搜索 tool 返回 id。
- resource URI 读取正文。
- prompt 启动常见工作流，例如“创建项目上下文”。
