---
name: context-engineering
description: "上下文工程技能：为 AI 编程、Agent、RAG 和长任务选择、压缩、组织上下文。Use when handling token budget/context window/memory/retrieval/long-horizon coding/context packs."
---

# Context Engineering

上下文工程的目标是控制“哪些信息、以什么结构、在什么时候”
进入模型，而不是把所有材料一次性塞进上下文。

## 使用场景

- 设计 MCP、Agent 或 AI 编程工具的上下文加载策略。
- 为长任务压缩历史记录、代码库信息、文档和工具结果。
- 决定 prompt、skill、doc、reference 的加载顺序。
- 设计 memory、retrieval、note、trace、summary 等机制。

## 工作流

1. 明确任务：生成代码、审查、调试、写计划、问答还是研究。
2. 列出信息源：用户需求、仓库文件、历史对话、文档、工具结果。
3. 分层上下文：系统规则、任务目标、当前状态、证据、候选资料。
4. 先检索后读取：先拿 metadata，再读取必要正文。
5. 压缩历史：保留决策、约束、未完成事项、验证结果。
6. 控制工具结果：大输出要摘要、分页、定位到行号或章节。
7. 设置刷新点：每个阶段结束写任务笔记，避免后续丢失状态。
8. 验证上下文：检查是否缺少目标、约束、输入、验收标准。

## 上下文包模板

```markdown
## 任务目标

## 当前状态

## 必须遵守的约束

## 已确认事实

## 相关文件或资源

## 待解决问题

## 验收标准

## 下一步动作
```

## 常见错误

- 把长文档全文返回给模型，而不是先返回摘要和定位信息。
- 对搜索结果没有评分、来源和命中字段，导致模型无法判断可信度。
- 只保存聊天记录，不保存决策、假设、验证命令和失败原因。
- 对工具结果不分页，导致单次调用挤掉核心任务上下文。
- 引入多份重复规则，让模型在冲突规则中摇摆。

## 参考资料

- `references/context-layers.md`：上下文分层和加载策略。
- `references/compression.md`：压缩、记忆和长任务维护。
- `references/source-map.md`：来源与许可证。
