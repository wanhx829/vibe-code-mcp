---
name: prompt-engineering
description: "Prompt Engineering 技能：设计、审查和优化提示词、系统提示词、角色提示词和任务模板。Use when writing prompts, prompt modules, system instructions, CoT/Self-Consistency, prompt evaluation."
---

# Prompt Engineering

用于把模糊自然语言需求转成稳定、可复用、可评估的提示词。

## 使用场景

- 设计系统提示词、角色提示词、工作流提示词。
- 优化现有 prompt 的结构、触发条件、输出格式和约束。
- 为 RAG、Agent、代码生成、审查和调试写 prompt。
- 拆分超长 prompt，形成模块化 prompt 包。

## Prompt 结构

推荐顺序：

1. 角色与任务边界。
2. 输入说明。
3. 必须遵守的约束。
4. 工作流程。
5. 输出格式。
6. 质量标准。
7. 示例。
8. 失败或不确定时的处理方式。

## 优化流程

1. 明确目标：prompt 要让模型产出什么。
2. 删除噪音：去掉重复、情绪化、无效强化词。
3. 补输入契约：用户需要提供什么，不提供时怎么问。
4. 写流程：把“思考方式”转成可执行步骤。
5. 固定输出：用 Markdown、JSON schema 或表格约束结果。
6. 加验收：列出自检清单和错误处理。
7. 用样例测试：至少准备 3 个典型输入和 2 个边界输入。

## 常见模块

- 任务描述补全。
- 需求澄清。
- 架构设计。
- 代码生成。
- 代码审查。
- 调试定位。
- 测试生成。
- 文档生成。
- 上下文压缩。

## 参考资料

- `references/prompt-patterns.md`：常见 prompt 模式。
- `references/evaluation.md`：prompt 评估方法。
- `references/source-map.md`：来源与许可证。
