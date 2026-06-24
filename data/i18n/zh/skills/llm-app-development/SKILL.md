---
name: llm-app-development
description: "LLM 应用开发技能：设计聊天、工具调用、RAG、Agent、评估、配置和部署。Use when building LLM apps with API/LangChain/tools/functions/streaming/memory/evaluation."
---

# LLM App Development

用于把 LLM 能力集成进真实应用，而不是停留在单次 prompt 调用。

## 使用场景

- 设计聊天助手、知识库问答、工具调用应用或 Agent 应用。
- 接入模型 API、函数调用、流式输出、记忆和检索。
- 规划配置、日志、成本、错误处理和部署。
- 从 demo 升级到可维护应用。

## 架构模块

1. 输入层：用户消息、文件、上下文、权限。
2. 编排层：prompt、工具、RAG、Agent loop、状态。
3. 模型层：模型选择、参数、重试、流式输出。
4. 工具层：函数调用、外部 API、MCP。
5. 数据层：向量库、数据库、对象存储、日志。
6. 评估层：测试集、trace、LLM-as-judge、人工抽检。
7. 运维层：配置、监控、成本、限流、安全。

## 实施流程

1. 写清用户场景和不可接受失败。
2. 先做最小对话或问答链路。
3. 加入结构化 prompt 和输出 schema。
4. 加入工具或检索。
5. 加入日志和 trace。
6. 建立评估集。
7. 再做流式输出、缓存、权限和部署。

## 交付清单

- 架构图。
- prompt 和工具 schema。
- 配置项说明。
- 错误处理策略。
- 评估样例。
- 部署和回滚方式。

## 参考资料

- `references/app-architecture.md`：应用架构。
- `references/evaluation-ops.md`：评估与运维。
- `references/source-map.md`：来源与许可证。
