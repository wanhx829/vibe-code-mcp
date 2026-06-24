# MCP 测试与调试

## 最小测试集

每个工具至少覆盖：

- 正常调用。
- 缺少必填参数。
- 空结果。
- 大结果。
- 外部依赖失败。

## 端到端调试

常用路径：

```bash
python server.py
npx @modelcontextprotocol/inspector python server.py
```

调试时检查：

- tools 是否正确注册。
- schema 是否符合预期。
- 参数默认值是否生效。
- 返回结构是否稳定。
- stderr 是否污染 stdio 协议。

## stdio 注意事项

- 协议数据走 stdout，不要打印普通日志到 stdout。
- 日志写 stderr。
- 启动阶段失败要给出清晰错误。
- 长任务要避免阻塞整个 server。

## MCP 客户端集成

配置中要明确：

- command。
- args。
- env。
- 工作目录或资源路径。
- Python/Node 版本要求。
