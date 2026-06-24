---
name: agent-engineering
description: "AI Agent 工程技能：设计、实现、评估和交付智能体系统。Use when building Agent/多智能体/工具调用/记忆/RAG/自主工作流/Agent 项目方案。"
---

# Agent Engineering

用于把“调用大模型”升级为可运行、可观察、可评估的 Agent 系统。

## 使用场景

- 设计 ReAct、Plan-and-Solve、Reflection、Supervisor、Handoff 等 Agent。
- 给 Agent 选择工具、记忆、检索、权限、状态和执行循环。
- 把用户需求拆成 Agent 项目方案、模块边界和验收指标。
- 评估 Agent 是否可靠，是否存在工具误用、上下文膨胀或安全风险。

## 快速流程

1. 定义任务环境：用户目标、输入输出、成功标准、失败代价。
2. 选择 Agent 范式：简单任务用 workflow，动态任务用 Agent loop。
3. 设计七层 harness：模型、循环、工具、记忆、人格、通道、自驱。
4. 列出工具能力：工具名、参数、返回值、权限、失败模式。
5. 设计状态和记忆：短期上下文、长期记忆、任务笔记、检索索引。
6. 写出执行循环：观察、思考、行动、记录、验证、停止条件。
7. 加入评估：任务成功率、工具调用准确率、成本、延迟、安全事件。
8. 给出最小可运行版本，再规划扩展能力。

## 方案模板

```markdown
## Agent 目标

## 任务环境

## 架构选择

## 工具清单

## 状态与记忆

## 执行循环

## 失败处理

## 评估指标

## 最小实现计划
```

## 设计原则

- 优先 workflow，只有任务需要动态决策时才引入 Agent loop。
- 工具越强，权限越要窄；读写工具分离，危险操作显式确认。
- 记忆必须可解释、可删除、可压缩，不把全部历史塞回上下文。
- 每个 Agent 都要有停止条件，避免无限循环和重复调用。
- 多智能体只在职责真正不同、可独立验收时使用。

## 典型产物

- Agent 系统架构图。
- 工具 schema 和权限表。
- 状态机或执行循环说明。
- 评估集和失败案例清单。
- 最小可运行实现计划。

## 参考资料

- `references/source-map.md`：外部来源与许可证记录。
- `references/agent-patterns.md`：Agent 范式与 harness 设计。
- `references/evaluation.md`：评估、观测和安全边界。
