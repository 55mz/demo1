# LangChain Agent Framework

一个最小但可扩展的 LangChain Agent 项目框架，适合继续接入业务工具、记忆、RAG、API 调用或多 Agent 编排。

## 目录结构

```text
.
├── pyproject.toml
├── .env.example
├── src/
│   └── agent_app/
│       ├── agent.py
│       ├── cli.py
│       ├── config.py
│       ├── llm.py
│       ├── prompts.py
│       ├── rag.py
│       ├── rag_tools.py
│       └── tools.py
└── tests/
    └── test_agent_framework.py
```

## 快速开始

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
Copy-Item .env.example .env
```

编辑 `.env`，填入：

```text
DEEPSEEK_API_KEY=你的 DeepSeek API Key
DEEPSEEK_MODEL=deepseek-chat
DEEPSEEK_TEMPERATURE=0
RAG_EMBEDDING_MODEL=BAAI/bge-small-zh-v1.5
```

把 `.txt`、`.md` 或 `.markdown` 文档放入 `workspace/input`，然后建立向量索引：

```powershell
ingest
```

首次运行会下载本地 HuggingFace embedding 模型，索引会保存到 `workspace/index/chroma`。

运行交互式 Agent：

```powershell
agent
```

或执行单条任务：

```powershell
agent "请计算 23 * 19，然后总结一句话"
```

询问本地文档：

```powershell
agent "根据本地文档总结项目的主要内容，并注明来源"
```

## 扩展方式

- 在 `src/agent_app/tools.py` 里添加新的 `@tool` 函数，并放进 `build_tools()` 返回列表。
- 在 `src/agent_app/prompts.py` 里调整系统提示词。
- 在 `src/agent_app/llm.py` 里替换模型供应商或模型参数。
- 在 `src/agent_app/agent.py` 里接入记忆、checkpoint、LangGraph 或自定义执行策略。

## 测试

```powershell
pytest
```
