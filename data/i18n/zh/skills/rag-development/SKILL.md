---
name: rag-development
description: "RAG 开发技能：设计检索增强生成系统、文档解析、分块、Embedding、Rerank、引用、评估和故障排查。Use when building RAG/知识库问答/文档检索/GraphRAG/Agentic RAG."
---

# RAG Development

用于构建可靠的检索增强生成系统，而不是只把文档塞进向量库。

## 使用场景

- 设计知识库问答、文档检索、企业搜索。
- 选择文档解析、分块、Embedding、Rerank 和引用策略。
- 诊断召回差、幻觉、引用错误、上下文过长等问题。
- 把 RAG 接入 Agent 或 MCP。

## 标准流程

1. 定义问题类型：事实问答、流程查询、代码检索、报告生成。
2. 分析数据源：格式、更新频率、权限、结构化程度。
3. 解析文档：保留标题、章节、表格、代码块和元数据。
4. 分块：按语义和结构分块，不只按固定字符数。
5. 建索引：Embedding、关键词、混合检索按场景选择。
6. 检索：query rewrite、query decomposition、top-k、过滤。
7. 重排：用 rerank 或规则提升相关性。
8. 生成：强制引用证据，无法回答时说明缺口。
9. 评估：召回率、答案正确性、引用准确性、成本和延迟。

## 设计检查

- 每个 chunk 是否有来源路径、标题、章节和更新时间。
- 查询是否支持同义词、缩写和中英文混合。
- 答案是否能追溯到具体证据。
- 是否区分“未检索到”和“检索到但无法回答”。
- 是否有权限过滤，避免跨用户泄露。

## 参考资料

- `references/pipeline.md`：RAG 全流程。
- `references/evaluation.md`：评估和排错。
- `references/source-map.md`：来源与许可证。
