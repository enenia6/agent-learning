# Agent Learning

从零手写一个最小 Agent Loop，再用 openai-agents 框架重构，理解 Agent 内部到底怎么跑起来的。

## 项目结构

| 文件 | 说明 |
|---|---|
| `minimal_agent.py` | 纯手写的最小 Agent（~150行），不依赖任何框架 |
| `first_agent.py` | 用 openai-agents 重写的版本（~45行） |
| `session_demo.py` | 多轮对话记忆（SQLiteSession） |
| `file_agent.py` | 带文件读取工具的文档助手雏形 |

## 跑起来

```bash
pip install openai openai-agents
# 填入你的阿里云百炼 API Key
python first_agent.py
```

## 核心理解

Agent 本质就是一个 while 循环：

```
调模型 → 模型要调工具 → 执行工具 → 结果塞回 messages → 再调一次
     → 模型不再要工具 → 输出最终答案，退出循环
```

关键概念：
- **messages**：对话历史，一个不断变长的列表（system/user/assistant/tool 四种角色）
- **tool_calls**：模型"点菜"，真正执行的是 Python 代码
- **Session**：把 messages 存到 SQLite，支持多轮对话
- **错误处理**：工具报错不崩，把错误信息喂回模型让它自己决定下一步

## 技术栈

- Python 3.13
- openai-agents（OpenAI 官方 Agent SDK）
- 阿里云百炼（通义千问 qwen-plus）
- SQLite（Session 持久化）
