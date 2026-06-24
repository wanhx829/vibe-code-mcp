# LLM 应用架构

## 最小应用

```text
User -> API -> Prompt Builder -> LLM -> Response
```

适合原型，不适合生产。

## 工具调用应用

```text
User -> Orchestrator -> LLM -> Tool Call -> Tool Result -> LLM -> Answer
```

关键点：

- 工具 schema 稳定。
- 工具结果要可信度标记。
- 工具失败要能恢复。

## RAG 应用

```text
User -> Query Rewrite -> Retriever -> Reranker -> Prompt -> LLM -> Answer
```

关键点：

- 证据必须带来源。
- 生成阶段限制在证据内。
- 无证据时拒答。

## Agent 应用

```text
User -> State -> Plan -> Tool Loop -> Memory -> Evaluation -> Answer
```

关键点：

- 有停止条件。
- 工具权限可控。
- 运行轨迹可回放。
