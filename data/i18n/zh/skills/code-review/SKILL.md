---
name: code-review
description: "代码审查技能：审查 bug、风险、回归、测试缺口、安全、可维护性和中文团队 review 表达。Use when reviewing code, PRs, diffs, architecture changes, generated code."
---

# Code Review

用于以工程风险为中心审查代码，而不是只做风格点评。

## 使用场景

- 审查 PR、diff、补丁或生成代码。
- 检查 bug、回归、安全、性能、可维护性和测试缺口。
- 给中文团队写清晰但不过度冒犯的 review 评论。
- 评估 AI 生成代码是否可合入。

## 审查顺序

1. 先理解变更目标和影响面。
2. 看入口、边界、错误处理和数据流。
3. 检查行为回归和兼容性。
4. 检查测试是否覆盖主路径和边界。
5. 检查安全、权限、并发、性能。
6. 最后看命名、风格和可读性。

## 输出格式

优先输出问题清单：

```markdown
## Findings

### [严重级别] 标题

- 位置：`path/to/file:line`
- 问题：
- 影响：
- 建议：
- 测试：

## Open Questions

## Summary
```

如果没有发现问题，明确说“未发现阻塞问题”，并说明剩余风险。

## 严重级别

- Blocker：会导致数据丢失、安全漏洞、核心流程不可用。
- High：明显 bug、回归、权限绕过、严重性能问题。
- Medium：边界缺失、错误处理不足、测试缺口。
- Low：可维护性、命名、注释、局部优化。

## 中文表达

- 用事实和影响说话，不做人身评价。
- 用“建议考虑”表达方案，但严重级别必须明确。
- 不确定时标记为“问题”，先询问意图。
- 不要因为语气温和而弱化阻塞问题。

## 参考资料

- `references/review-checklist.md`：审查清单。
- `references/chinese-review-style.md`：中文 review 表达。
- `references/source-map.md`：来源与许可证。
